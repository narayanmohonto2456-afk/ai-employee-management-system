from django.contrib import admin

from .models import Attendance


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    """
    Admin configuration for Attendance.
    """

    list_display = (
        "employee",
        "date",
        "check_in",
        "check_out",
        "working_hours",
        "status",
    )

    list_filter = (
        "status",
        "date",
    )

    search_fields = (
        "employee__employee_id",
        "employee__user__first_name",
        "employee__user__last_name",
        "employee__user__username",
    )

    ordering = (
        "-date",
        "-id",
    )

    date_hierarchy = "date"

    list_per_page = 20