from django.contrib import admin

from .models import Department


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Department model.
    """

    list_display = (
        "department_name",
        "department_code",
        "created_at",
        "updated_at",
    )

    search_fields = (
        "department_name",
        "department_code",
    )

    list_filter = (
        "created_at",
        "updated_at",
    )

    ordering = (
        "department_name",
    )

    list_per_page = 10

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    fieldsets = (
        (
            "Department Information",
            {
                "fields": (
                    "department_name",
                    "department_code",
                    "description",
                ),
            },
        ),
        (
            "System Information",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                ),
            },
        ),
    )