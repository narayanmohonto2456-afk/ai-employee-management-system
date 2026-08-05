from django.contrib import admin
from .models import Employee


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    """
    Employee Admin Configuration
    """

    list_display = (
        "employee_id",
        "user",
        "department",
        "designation",
        "joining_date",
    )

    list_filter = (
        "department",
        "gender",
        "joining_date",
    )

    search_fields = (
        "employee_id",
        "user__username",
        "user__first_name",
        "user__last_name",
        "designation",
    )

    ordering = (
        "employee_id",
    )

    list_per_page = 20