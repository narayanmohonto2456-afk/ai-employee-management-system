from django.urls import path

from .views import (
    DepartmentListView,
    DepartmentDetailView,
    DepartmentCreateView,
    DepartmentUpdateView,
    DepartmentDeleteView,
)

app_name = "departments"

urlpatterns = [
    # List all departments
    path(
        "",
        DepartmentListView.as_view(),
        name="department_list",
    ),

    # Create department
    path(
        "create/",
        DepartmentCreateView.as_view(),
        name="department_create",
    ),

    # Department details
    path(
        "<int:pk>/",
        DepartmentDetailView.as_view(),
        name="department_detail",
    ),

    # Update department
    path(
        "<int:pk>/update/",
        DepartmentUpdateView.as_view(),
        name="department_update",
    ),

    # Delete department
    path(
        "<int:pk>/delete/",
        DepartmentDeleteView.as_view(),
        name="department_delete",
    ),
]