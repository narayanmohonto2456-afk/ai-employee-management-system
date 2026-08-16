from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.http import HttpResponse
from django.core.exceptions import PermissionDenied

from .utils import (
    generate_attendance_excel,
    generate_attendance_pdf,
)

from attendance.models import Attendance
from departments.models import Department
from employees.models import Employee
from django.views.generic import TemplateView, View


class AttendanceReportMixin(LoginRequiredMixin):
    """
    Common authorization and queryset logic for attendance reports.

    ADMIN:
        Can see all attendance records.

    HR:
        Can see all attendance records.

    EMPLOYEE:
        Can see only their own attendance records.
    """

    def get_attendance_queryset(self):

        queryset = Attendance.objects.select_related(
            "employee",
            "employee__user",
            "employee__department",
        ).order_by("-date", "-id")

        user = self.request.user

        # ----------------------------------------------------
        # Employee
        # ----------------------------------------------------

        if user.role == "EMPLOYEE":

            queryset = queryset.filter(
                employee__user=user
            )

        # ----------------------------------------------------
        # Admin / HR
        # ----------------------------------------------------

        elif user.role in ["ADMIN", "HR"]:

            pass

        # ----------------------------------------------------
        # Unknown role
        # ----------------------------------------------------

        else:

            raise PermissionDenied(
                "You do not have permission to access attendance reports."
            )

        return queryset

    def apply_filters(self, queryset):

        employee = self.request.GET.get("employee")
        department = self.request.GET.get("department")
        status = self.request.GET.get("status")
        start_date = self.request.GET.get("start_date")
        end_date = self.request.GET.get("end_date")

        # ----------------------------------------------------
        # Employee filter
        # ----------------------------------------------------

        if employee:

            queryset = queryset.filter(
                employee__employee_id__icontains=employee
            )

        # ----------------------------------------------------
        # Department filter
        # ----------------------------------------------------

        if department:

            queryset = queryset.filter(
                employee__department_id=department
            )

        # ----------------------------------------------------
        # Status filter
        # ----------------------------------------------------

        if status:

            queryset = queryset.filter(
                status=status
            )

        # ----------------------------------------------------
        # Start date
        # ----------------------------------------------------

        if start_date:

            queryset = queryset.filter(
                date__gte=start_date
            )

        # ----------------------------------------------------
        # End date
        # ----------------------------------------------------

        if end_date:

            queryset = queryset.filter(
                date__lte=end_date
            )

        return queryset


class AttendanceReportView(
    AttendanceReportMixin,
    TemplateView,
):
    """
    Attendance report page.

    Admin:
        All employees.

    HR:
        All employees.

    Employee:
        Own attendance only.
    """

    template_name = "reports/attendance_report.html"

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        queryset = self.get_attendance_queryset()

        queryset = self.apply_filters(queryset)

        context["attendance_records"] = queryset

        # ----------------------------------------------------
        # Filter options
        # ----------------------------------------------------

        if self.request.user.role in ["ADMIN", "HR"]:

            context["departments"] = Department.objects.all()

            context["employees"] = Employee.objects.select_related(
                "user"
            )

        else:

            context["departments"] = Department.objects.filter(
                id__in=queryset.values_list(
                    "employee__department_id",
                    flat=True,
                ).distinct()
            )

            context["employees"] = Employee.objects.filter(
                user=self.request.user
            ).select_related("user")

        # ----------------------------------------------------
        # Statistics
        # ----------------------------------------------------

        context["total_records"] = queryset.count()

        context["present_count"] = queryset.filter(
            status=Attendance.StatusChoices.PRESENT
        ).count()

        context["absent_count"] = queryset.filter(
            status=Attendance.StatusChoices.ABSENT
        ).count()

        context["leave_count"] = queryset.filter(
            status=Attendance.StatusChoices.LEAVE
        ).count()

        context["half_day_count"] = queryset.filter(
            status=Attendance.StatusChoices.HALF_DAY
        ).count()

        # ----------------------------------------------------
        # Current filter values
        # ----------------------------------------------------

        context["selected_employee"] = (
            self.request.GET.get("employee", "")
        )

        context["selected_department"] = (
            self.request.GET.get("department", "")
        )

        context["selected_status"] = (
            self.request.GET.get("status", "")
        )

        context["selected_start_date"] = (
            self.request.GET.get("start_date", "")
        )

        context["selected_end_date"] = (
            self.request.GET.get("end_date", "")
        )

        return context


class AttendanceExcelExportView(
    AttendanceReportMixin, View,
):
    """
    Export attendance report to Excel.

    Uses exactly the same authorization and
    filtering logic as the attendance report page.
    """

    def get(self, request, *args, **kwargs):

        queryset = self.get_attendance_queryset()

        queryset = self.apply_filters(queryset)

        workbook = generate_attendance_excel(
            queryset
        )

        response = HttpResponse(
            content_type=(
                "application/vnd.openxmlformats-officedocument."
                "spreadsheetml.sheet"
            )
        )

        response[
            "Content-Disposition"
        ] = (
            'attachment; '
            'filename="attendance_report.xlsx"'
        )

        workbook.save(response)

        return response


class AttendancePDFExportView(
    AttendanceReportMixin,View,
):
    """
    Export attendance report to PDF.

    Uses exactly the same authorization and
    filtering logic as the attendance report page.
    """

    def get(self, request, *args, **kwargs):

        queryset = self.get_attendance_queryset()

        queryset = self.apply_filters(queryset)

        response = HttpResponse(
            content_type="application/pdf"
        )

        response[
            "Content-Disposition"
        ] = (
            'attachment; '
            'filename="attendance_report.pdf"'
        )

        generate_attendance_pdf(
            response,
            queryset,
        )

        return response