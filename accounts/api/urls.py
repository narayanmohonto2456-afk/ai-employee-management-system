from django.urls import path

from .views import (LoginAPIView,
                     LogoutAPIView, 
                     UserProfileAPIView, 
                     ChangePasswordAPIView,
                     VerifyEmailAPIView,
                     RegisterAPIView
                     )

app_name = "accounts_api"

urlpatterns = [

    path(
        "login/",
        LoginAPIView.as_view(),
        name="login",
    ),

    path(
    "logout/",
    LogoutAPIView.as_view(),
    name="logout",
),

path("profile/", UserProfileAPIView.as_view(), name="profile"),
path("change-password/", ChangePasswordAPIView.as_view(), name="change_password"),
path("verify-email/<uid>/<token>/", VerifyEmailAPIView.as_view(), name="verify_email",),
path("register/", RegisterAPIView.as_view(), name="register",),

]