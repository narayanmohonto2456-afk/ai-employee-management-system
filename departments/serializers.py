from rest_framework import serializers

from .models import Department


class DepartmentSerializer(serializers.ModelSerializer):

#    Serializer for Department API.


    class Meta:
        model = Department

        fields = [
            "id",
            "department_name",
            "department_code",
            "description",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]