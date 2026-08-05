from django.contrib import admin

from .models import Leave, LeaveType


@admin.register(LeaveType)
class LeaveTypeAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
    )


@admin.register(Leave)
class LeaveAdmin(admin.ModelAdmin):
    list_display = (
        "employee",
        "leave_type",
        "start_date",
        "end_date",
        "status",
    )

    list_filter = (
        "status",
        "leave_type",
    )

    search_fields = (
        "employee__employee_id",
        "employee__user__username",
    )