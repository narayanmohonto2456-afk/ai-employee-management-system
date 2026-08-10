from django.urls import path

from .views import (LoginAPIView,
                     LogoutAPIView, 
                     UserProfileAPIView, 
                     ChangePasswordAPIView,
                     VerifyEmailAPIView,
                     RegisterAPIView,
                     ResendVerificationEmailAPIView,
                     ForgotPasswordAPIView,
                     ResetPasswordAPIView
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
path("resend-verification/", ResendVerificationEmailAPIView.as_view(), name="resend_verification"),
path("forgot-password/", ForgotPasswordAPIView.as_view(), name="forgot_password",),
path("reset-password/",ResetPasswordAPIView.as_view(),name="reset_password",),

]