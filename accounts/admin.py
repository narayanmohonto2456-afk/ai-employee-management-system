from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """
    Custom Admin configuration for the User model.
    """

    # Columns shown in the user list
    list_display = (
        "id",
        "username",
        "email",
        "first_name",
        "last_name",
        "phone",
        "role",
        "is_staff",
        "is_active",
    )

    # Filters on the right side
    list_filter = (
        "role",
        "is_staff",
        "is_active",
        "is_superuser",
        "groups",
    )

    # Search box
    search_fields = (
        "username",
        "email",
        "first_name",
        "last_name",
        "phone",
    )

    # Default ordering
    ordering = ("username",)

    # Read-only fields
    readonly_fields = (
        "last_login",
        "date_joined",
    )

    # User edit page
    fieldsets = (
        ("Login Information", {
            "fields": (
                "username",
                "password",
            )
        }),

        ("Personal Information", {
            "fields": (
                "first_name",
                "last_name",
                "email",
                "phone",
                "profile_image",
                "role",
            )
        }),

        ("Permissions", {
            "fields": (
                "is_active",
                "is_staff",
                "is_superuser",
                "groups",
                "user_permissions",
            )
        }),

        ("Important Dates", {
            "fields": (
                "last_login",
                "date_joined",
            )
        }),
    )

    # User creation page
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "email",
                    "phone",
                    "role",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_active",
                ),
            },
        ),
    )