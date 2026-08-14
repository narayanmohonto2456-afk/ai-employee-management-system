from django.urls import path

from employees.views import (
    EmployeeListCreateAPIView,
    EmployeeDetailAPIView,
)


app_name = "employees_api"


urlpatterns = [
    path(
        "",
        EmployeeListCreateAPIView.as_view(),
        name="employee_list_create",
    ),

    path(
        "<int:pk>/",
        EmployeeDetailAPIView.as_view(),
        name="employee_detail",
    ),
]