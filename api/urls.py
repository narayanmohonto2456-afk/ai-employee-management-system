from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import (
    UserProfileAPIView,
    EmployeeListCreateAPIView,
    EmployeeDetailAPIView,
    MyEmployeeProfileAPIView,
)
app_name = "api"

urlpatterns = [

    path(
        "token/",
        TokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),

    path(
        "token/refresh/",
        TokenRefreshView.as_view(),
        name="token_refresh",
    ),

    path(
        "profile/",
        UserProfileAPIView.as_view(),
        name="profile",
    ),
path(
    "employees/",
    EmployeeListCreateAPIView.as_view(),
    name="employee_list",
),

path(
    "employees/<int:pk>/",
    EmployeeDetailAPIView.as_view(),
    name="employee_detail",
),
path(
    "my-profile/",
    MyEmployeeProfileAPIView.as_view(),
    name="my_profile",
),
]