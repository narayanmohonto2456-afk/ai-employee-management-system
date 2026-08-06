from django.contrib.auth import get_user_model
from rest_framework import serializers

from departments.models import Department
from employees.models import Employee


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for authenticated user details.
    """

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "is_staff",
            "is_superuser",
        )
        read_only_fields = fields


class DepartmentSerializer(serializers.ModelSerializer):
    """
    Serializer for Department.
    """

    class Meta:
        model = Department

        fields = (
            "id",
            "department_name",
            "department_code",
            "description",
            "created_at",
            "updated_at",
        )

        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
        )

class EmployeeSerializer(serializers.ModelSerializer):
    """
    Serializer for Employee.
    """

    user_name = serializers.CharField(
        source="user.get_full_name",
        read_only=True,
    )

    department_name = serializers.CharField(
        source="department.department_name",
        read_only=True,
    )

    class Meta:
        model = Employee

        fields = (
            "id",
            "employee_id",
            "user",
            "user_name",
            "department",
            "department_name",
            "designation",
            "gender",
            "date_of_birth",
            "joining_date",
            "address",
            "city",
            "state",
            "country",
            "profile_picture",
            "created_at",
            "updated_at",
        )

        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
        )