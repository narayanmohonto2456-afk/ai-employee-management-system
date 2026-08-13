from django.urls import path

from departments.views import (
    DepartmentListCreateAPIView,
    DepartmentDetailAPIView,
)


app_name = "departments_api"


urlpatterns = [
    path(
        "",
        DepartmentListCreateAPIView.as_view(),
        name="department_list_create",
    ),

    path(
        "<int:pk>/",
        DepartmentDetailAPIView.as_view(),
        name="department_detail",
    ),
]