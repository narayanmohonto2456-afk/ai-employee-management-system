from django.urls import path

from .views import (
    LeaveListView,
    LeaveDetailView,
    LeaveCreateView,
    LeaveUpdateView,
    approve_leave,
    reject_leave,
)
app_name = "leave_management"

urlpatterns = [
    path(
        "",
        LeaveListView.as_view(),
        name="leave_list",
    ),

    path(
        "create/",
        LeaveCreateView.as_view(),
        name="leave_create",
    ),
    path(
    "<int:pk>/approve/",
    approve_leave,
    name="approve_leave",
),

path(
    "<int:pk>/reject/",
    reject_leave,
    name="reject_leave",
),

    path(
        "<int:pk>/",
        LeaveDetailView.as_view(),
        name="leave_detail",
    ),

    path(
        "<int:pk>/update/",
        LeaveUpdateView.as_view(),
        name="leave_update",
    ),
]