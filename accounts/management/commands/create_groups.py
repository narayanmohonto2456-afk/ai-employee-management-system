from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission


class Command(BaseCommand):
    help = "Create default EMS groups and assign permissions"

    def handle(self, *args, **kwargs):

        # Create Groups
        super_admin, _ = Group.objects.get_or_create(name="Super Admin")
        hr_manager, _ = Group.objects.get_or_create(name="HR Manager")
        manager, _ = Group.objects.get_or_create(name="Manager")
        employee, _ = Group.objects.get_or_create(name="Employee")

        # Super Admin -> All Permissions
        super_admin.permissions.set(Permission.objects.all())

        # HR Manager Permissions
        hr_permissions = Permission.objects.filter(
            content_type__app_label__in=[
                "employees",
                "departments",
                "attendance",
                "leave_management",
            ]
        )
        hr_manager.permissions.set(hr_permissions)

        # Manager Permissions
        manager_permissions = Permission.objects.filter(
            content_type__app_label__in=[
                "attendance",
                "leave_management",
            ]
        )
        manager.permissions.set(manager_permissions)

        # Employee Permissions
        employee_permissions = Permission.objects.filter(
            codename__in=[
                "view_employee",
                "view_attendancerecord",
            ]
        )
        employee.permissions.set(employee_permissions)

        self.stdout.write(
            self.style.SUCCESS(
                "Groups and permissions assigned successfully."
            )
        )