from django.urls import path

from .views import (
    AttendanceListView,
    AttendanceCreateView,
    AttendanceUpdateView,
    AttendanceDetailView,
    AttendanceDeleteView,
    CheckInView,
    CheckOutView,
)

app_name = "attendance"

urlpatterns = [
    path(
        "",
        AttendanceListView.as_view(),
        name="attendance_list",
    ),

    path(
        "create/",
        AttendanceCreateView.as_view(),
        name="attendance_create",
    ),

    path(
        "<int:pk>/",
        AttendanceDetailView.as_view(),
        name="attendance_detail",
    ),

    path(
        "<int:pk>/update/",
        AttendanceUpdateView.as_view(),
        name="attendance_update",
    ),

    path(
        "<int:pk>/delete/",
        AttendanceDeleteView.as_view(),
        name="attendance_delete",
    ),

    path(
        "check-in/",
        CheckInView.as_view(),
        name="check_in",
    ),

    path(
        "check-out/",
        CheckOutView.as_view(),
        name="check_out",
    ),
]