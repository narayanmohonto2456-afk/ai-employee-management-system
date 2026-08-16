from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.utils import timezone

from departments.models import Department
from employees.models import Employee
from attendance.models import Attendance
from leave_management.models import Leave


class DashboardView(
    LoginRequiredMixin,
    TemplateView,
):

    template_name = "dashboard/dashboard.html"

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        user = self.request.user
        today = timezone.localdate()

        # ====================================================
        # ADMIN / HR DASHBOARD
        # ====================================================

        if user.role in ["ADMIN", "HR"]:

            context["employee_count"] = (
                Employee.objects.count()
            )

            context["department_count"] = (
                Department.objects.count()
            )

            context["leave_count"] = (
                Leave.objects.count()
            )

            context["attendance_count"] = (
                Attendance.objects.count()
            )

            # -----------------------------------------------
            # Today's attendance
            # -----------------------------------------------

            context["today_present"] = Attendance.objects.filter(
                date=today,
                status=Attendance.StatusChoices.PRESENT,
            ).count()

            context["today_absent"] = Attendance.objects.filter(
                date=today,
                status=Attendance.StatusChoices.ABSENT,
            ).count()

            context["today_leave"] = Attendance.objects.filter(
                date=today,
                status=Attendance.StatusChoices.LEAVE,
            ).count()

            context["today_half_day"] = Attendance.objects.filter(
                date=today,
                status=Attendance.StatusChoices.HALF_DAY,
            ).count()

            # -----------------------------------------------
            # Overall attendance statistics
            # -----------------------------------------------

            context["present_count"] = Attendance.objects.filter(
                status=Attendance.StatusChoices.PRESENT
            ).count()

            context["absent_count"] = Attendance.objects.filter(
                status=Attendance.StatusChoices.ABSENT
            ).count()

            context["leave_attendance_count"] = (
                Attendance.objects.filter(
                    status=Attendance.StatusChoices.LEAVE
                ).count()
            )

            context["half_day_count"] = (
                Attendance.objects.filter(
                    status=Attendance.StatusChoices.HALF_DAY
                ).count()
            )

            # -----------------------------------------------
            # Recent employees
            # -----------------------------------------------

            context["recent_employees"] = (
                Employee.objects
                .select_related(
                    "user",
                    "department",
                )
                .order_by("-id")[:5]
            )

            # -----------------------------------------------
            # Recent leave applications
            # -----------------------------------------------

            context["recent_leaves"] = (
                Leave.objects
                .select_related(
                    "employee",
                    "employee__user",
                    "leave_type",
                )
                .order_by("-applied_at")[:5]
            )

        # ====================================================
        # EMPLOYEE DASHBOARD
        # ====================================================

        else:

            employee = Employee.objects.filter(
                user=user
            ).first()

            if employee:

                employee_attendance = Attendance.objects.filter(
                    employee=employee
                )

                employee_leaves = Leave.objects.filter(
                    employee=employee
                )

                # -------------------------------------------
                # Employee statistics
                # -------------------------------------------

                context["employee_count"] = 1

                context["department_count"] = 1

                context["attendance_count"] = (
                    employee_attendance.count()
                )

                context["leave_count"] = (
                    employee_leaves.count()
                )

                # -------------------------------------------
                # Today's attendance
                # -------------------------------------------

                context["today_present"] = (
                    employee_attendance.filter(
                        date=today,
                        status=Attendance.StatusChoices.PRESENT,
                    ).count()
                )

                context["today_absent"] = (
                    employee_attendance.filter(
                        date=today,
                        status=Attendance.StatusChoices.ABSENT,
                    ).count()
                )

                context["today_leave"] = (
                    employee_attendance.filter(
                        date=today,
                        status=Attendance.StatusChoices.LEAVE,
                    ).count()
                )

                context["today_half_day"] = (
                    employee_attendance.filter(
                        date=today,
                        status=Attendance.StatusChoices.HALF_DAY,
                    ).count()
                )

                # -------------------------------------------
                # Overall attendance
                # -------------------------------------------

                context["present_count"] = (
                    employee_attendance.filter(
                        status=Attendance.StatusChoices.PRESENT
                    ).count()
                )

                context["absent_count"] = (
                    employee_attendance.filter(
                        status=Attendance.StatusChoices.ABSENT
                    ).count()
                )

                context["leave_attendance_count"] = (
                    employee_attendance.filter(
                        status=Attendance.StatusChoices.LEAVE
                    ).count()
                )

                context["half_day_count"] = (
                    employee_attendance.filter(
                        status=Attendance.StatusChoices.HALF_DAY
                    ).count()
                )

                # -------------------------------------------
                # Employee's recent attendance
                # -------------------------------------------

                context["recent_employees"] = (
                    Employee.objects.filter(
                        pk=employee.pk
                    ).select_related(
                        "user",
                        "department",
                    )
                )

                # -------------------------------------------
                # Employee's recent leaves
                # -------------------------------------------

                context["recent_leaves"] = (
                    employee_leaves
                    .select_related(
                        "employee",
                        "employee__user",
                        "leave_type",
                    )
                    .order_by("-applied_at")[:5]
                )

            else:

                # User has no employee profile
                context["employee_count"] = 0
                context["department_count"] = 0
                context["attendance_count"] = 0
                context["leave_count"] = 0

                context["today_present"] = 0
                context["today_absent"] = 0
                context["today_leave"] = 0
                context["today_half_day"] = 0

                context["present_count"] = 0
                context["absent_count"] = 0
                context["leave_attendance_count"] = 0
                context["half_day_count"] = 0

                context["recent_employees"] = Employee.objects.none()
                context["recent_leaves"] = Leave.objects.none()

        return context