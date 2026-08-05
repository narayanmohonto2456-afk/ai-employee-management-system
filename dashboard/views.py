from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from departments.models import Department
from employees.models import Employee
from attendance.models import Attendance
from leave_management.models import Leave
from django.utils import timezone
from attendance.models import Attendance


class DashboardView(LoginRequiredMixin, TemplateView):

    template_name = "dashboard/dashboard.html"

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        today = timezone.localdate()

        context["employee_count"] = Employee.objects.count()
        context["department_count"] = Department.objects.count()
        context["leave_count"] = Leave.objects.count()

        # Attendance Statistics
        context["attendance_count"] = Attendance.objects.count()

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

        context["recent_employees"] = (
            Employee.objects
            .select_related("user", "department")
            .order_by("-id")[:5]
        )

        context["recent_leaves"] = (
            Leave.objects
            .select_related(
                "employee",
                "employee__user",
                "leave_type",
            )
            .order_by("-applied_at")[:5]
        )
        # Attendance Statistics

        context["present_count"] = Attendance.objects.filter(
            status=Attendance.StatusChoices.PRESENT
        ).count()

        context["absent_count"] = Attendance.objects.filter(
            status=Attendance.StatusChoices.ABSENT
        ).count()

        context["leave_attendance_count"] = Attendance.objects.filter(
            status=Attendance.StatusChoices.LEAVE
        ).count()

        context["half_day_count"] = Attendance.objects.filter(
            status=Attendance.StatusChoices.HALF_DAY
        ).count()

        return context