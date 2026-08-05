from django.urls import path

from .views import (
    EmployeeListView,
    EmployeeSearchAPIView,
    EmployeeDetailView,
    EmployeeCreateView,
    EmployeeUpdateView,
    EmployeeDeleteView,
)

app_name = "employees"

urlpatterns = [

    path(
        "",
        EmployeeListView.as_view(),
        name="employee_list",
    ),

    path(
    "search/",
    EmployeeSearchAPIView.as_view(),
    name="employee_search",
),

    path(
        "create/",
        EmployeeCreateView.as_view(),
        name="employee_create",
    ),

    path(
        "<int:pk>/",
        EmployeeDetailView.as_view(),
        name="employee_detail",
    ),

    path(
        "<int:pk>/update/",
        EmployeeUpdateView.as_view(),
        name="employee_update",
    ),

    path(
        "<int:pk>/delete/",
        EmployeeDeleteView.as_view(),
        name="employee_delete",
    ),

]