from rest_framework import status
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode

from accounts.tokens import email_verification_token

from .serializers import (LoginSerializer,
                          LogoutSerializer,
                          UserProfileSerializer, 
                          ChangePasswordSerializer, 
                          RegisterSerializer,
                          ResendVerificationEmailSerializer,
                          ForgotPasswordSerializer,
                          ResetPasswordSerializer,)

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from accounts.services.email_service import EmailService



User = get_user_model()

class RegisterAPIView(APIView):
    
#    Register a new user and send email verification.
    

    permission_classes = [AllowAny]

    def post(self, request):

        serializer = RegisterSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        user = serializer.save()

        EmailService.send_verification_email(
            request,
            user,
        )

        return Response(
            {
                "success": True,
                "message": (
                    "Registration successful. "
                    "Please check your email "
                    "to verify your account."
                ),
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "email_verified": user.email_verified,
                },
            },
            status=status.HTTP_201_CREATED,
        )

class LoginAPIView(TokenObtainPairView):

#    Login API using Simple JWT.

    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        return Response(
            serializer.validated_data,
            status=status.HTTP_200_OK,
        )

class LogoutAPIView(APIView):
# Logout API

    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = LogoutSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        serializer.save()

        return Response(
            {
                "message": "Logout successful."
            },
            status=status.HTTP_200_OK,
        )

class UserProfileAPIView(APIView):

#    Returns the currently authenticated user's profile.

    permission_classes = [IsAuthenticated]

    def get(self, request):

        serializer = UserProfileSerializer(request.user)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )

class ChangePasswordAPIView(APIView):

#    Change Password API

    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = ChangePasswordSerializer(
            data=request.data,
            context={
                "request": request
            },
        )

        serializer.is_valid(
            raise_exception=True
        )

        serializer.save()

        return Response(
            {
                "message": "Password changed successfully."
            },
            status=status.HTTP_200_OK,
        )
    


class VerifyEmailAPIView(APIView):
    
#    Verify user email.


    permission_classes = [AllowAny]

    def get(self, request, uid, token):

        try:

            user_id = force_str(
                urlsafe_base64_decode(uid)
            )

            user = User.objects.get(pk=user_id)

        except (
            TypeError,
            ValueError,
            OverflowError,
            User.DoesNotExist,
        ):

            return Response(
                {
                    "success": False,
                    "message": "Invalid verification link."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if email_verification_token.check_token(
            user,
            token,
        ):

            # Email verified
            user.email_verified = True
            user.save(update_fields=["email_verified"])

            return Response(
                {
                    "success": True,
                    "message": "Email verified successfully."
                }
            )

        return Response(
            {
                "success": False,
                "message": "Verification link has expired."
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

class ResendVerificationEmailAPIView(APIView):

    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):

        serializer = ResendVerificationEmailSerializer(
            data=request.data,
            context={"request": request},
        )

        serializer.is_valid(raise_exception=True)

        user = serializer.user

        EmailService.send_verification_email(
            request,
            user,
        )

        return Response(
            {
                "detail": (
                    "A new verification email "
                    "has been sent."
                )
            },
            status=status.HTTP_200_OK,
        )

class ForgotPasswordAPIView(APIView):

    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):

        serializer = ForgotPasswordSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        user = serializer.user

        EmailService.send_password_reset_email(
            request,
            user,
        )

        return Response(
            {
                "message": (
                    "Password reset email sent successfully."
                )
            },
            status=status.HTTP_200_OK,
        )

class ResetPasswordAPIView(APIView):

    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):

        serializer = ResetPasswordSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        user = serializer.user

        user.set_password(
            serializer.validated_data["new_password"]
        )

        user.save(
            update_fields=["password"]
        )

        return Response(
            {
                "message":
                "Password reset successfully."
            },
            status=status.HTTP_200_OK,
        )