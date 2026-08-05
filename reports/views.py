from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.http import HttpResponse

from .utils import (
    generate_attendance_excel,
    generate_attendance_pdf,
)
from attendance.models import Attendance
from departments.models import Department
from employees.models import Employee

class AttendanceReportView(LoginRequiredMixin, TemplateView):

    template_name = "reports/attendance_report.html"

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        queryset = Attendance.objects.select_related(
            "employee",
            "employee__user",
            "employee__department",
        ).order_by("-date")

        employee = self.request.GET.get("employee")
        department = self.request.GET.get("department")
        status = self.request.GET.get("status")
        start_date = self.request.GET.get("start_date")
        end_date = self.request.GET.get("end_date")

        if employee:
            queryset = queryset.filter(
                employee__employee_id__icontains=employee
            )

        if department:
            queryset = queryset.filter(
                employee__department_id=department
            )

        if status:
            queryset = queryset.filter(
                status=status
            )

        if start_date:
            queryset = queryset.filter(
                date__gte=start_date
            )

        if end_date:
            queryset = queryset.filter(
                date__lte=end_date
            )

        context["attendance_records"] = queryset
        context["departments"] = Department.objects.all()
        context["employees"] = Employee.objects.select_related(
            "user"
        )
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

        return context

class AttendanceExcelExportView(LoginRequiredMixin, TemplateView):

    def get(self, request, *args, **kwargs):

        queryset = Attendance.objects.select_related(
            "employee",
            "employee__user",
            "employee__department",
        ).order_by("-date")

        workbook = generate_attendance_excel(queryset)

        response = HttpResponse(
            content_type=(
                "application/vnd.openxmlformats-officedocument."
                "spreadsheetml.sheet"
            )
        )

        response[
            "Content-Disposition"
        ] = 'attachment; filename="attendance_report.xlsx"'

        workbook.save(response)

        return response

class AttendancePDFExportView(LoginRequiredMixin, TemplateView):

    def get(self, request, *args, **kwargs):

        queryset = Attendance.objects.select_related(
            "employee",
            "employee__user",
            "employee__department",
        ).order_by("-date")

        response = HttpResponse(
            content_type="application/pdf"
        )

        response[
            "Content-Disposition"
        ] = 'attachment; filename="attendance_report.pdf"'

        generate_attendance_pdf(
            response,
            queryset,
        )

        return response
    
