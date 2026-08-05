from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import (
    UserSerializer,
    DepartmentSerializer,
    EmployeeSerializer,
)
from rest_framework import generics, filters
from departments.models import Department
from django_filters.rest_framework import DjangoFilterBackend
from employees.models import Employee
from .permissions import IsAdminOrReadOnly

class UserProfileAPIView(APIView):
    """
    Returns the authenticated user's profile.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):

        serializer = UserSerializer(request.user)

        return Response(serializer.data)

class DepartmentListCreateAPIView(generics.ListCreateAPIView):
    """
    List all departments or create a new department.
    """
    permission_classes = [IsAdminOrReadOnly]
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    filterset_fields = [
        "department_name",
        "department_code",
    ]

    search_fields = [
        "department_name",
        "department_code",
    ]

    ordering_fields = [
        "department_name",
        "department_code",
        "created_at",
    ]

    ordering = [
        "department_name",
    ]

class DepartmentDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a department.
    """
    permission_classes = [IsAdminOrReadOnly]
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

class EmployeeListCreateAPIView(generics.ListCreateAPIView):
    """
    List all employees or create a new employee.
    """
    permission_classes = [IsAdminOrReadOnly]
    queryset = (
        Employee.objects
        .select_related("user", "department")
        .all()
    )

    serializer_class = EmployeeSerializer

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    filterset_fields = [
        "department",
        "designation",
        "gender",
    ]

    search_fields = [
        "employee_id",
        "user__first_name",
        "user__last_name",
        "user__username",
        "department__department_name",
        "designation",
    ]

    ordering_fields = [
        "employee_id",
        "joining_date",
        "created_at",
    ]

    ordering = [
        "employee_id",
    ]


class EmployeeDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete an employee.
    """
    permission_classes = [IsAdminOrReadOnly]
    queryset = (
        Employee.objects
        .select_related("user", "department")
        .all()
    )

    serializer_class = EmployeeSerializer

class MyEmployeeProfileAPIView(generics.RetrieveAPIView):
    """
    Returns the logged-in employee's profile.
    """

    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return Employee.objects.select_related(
            "user",
            "department",
        ).get(
            user=self.request.user
        )