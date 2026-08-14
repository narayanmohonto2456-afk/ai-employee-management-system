from rest_framework import serializers

from .models import Employee


class EmployeeSerializer(serializers.ModelSerializer):
    """
    Serializer for Employee model.
    """

    class Meta:
        model = Employee
        fields = [
            "id",
            "employee_id",
            "user",
            "department",
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
        ]

        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]