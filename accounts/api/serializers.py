from django.contrib.auth import authenticate

from rest_framework import serializers

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from accounts.models import User
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model
from accounts.services.email_service import EmailService
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        write_only=True,
        validators=[validate_password],
    )

    confirm_password = serializers.CharField(
        write_only=True,
    )

    class Meta:
        model = User

        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "phone",
            "password",
            "confirm_password",
        ]

    def validate(self, attrs):

        if attrs["password"] != attrs["confirm_password"]:
            raise serializers.ValidationError(
                {
                    "confirm_password":
                    "Passwords do not match."
                }
            )

        return attrs

    def create(self, validated_data):

        validated_data.pop("confirm_password")

        password = validated_data.pop("password")

        user = User.objects.create_user(
        password=password,
        **validated_data,
        )

        user.email_verified = False

        user.save(
            update_fields=["email_verified"]
        )

        return user

    
class LoginSerializer(serializers.Serializer):
    """
    Authenticate users using email address and password
    and return JWT access and refresh tokens.
    """

    email = serializers.EmailField(
        required=True
    )

    password = serializers.CharField(
        write_only=True,
        required=True,
    )

    def validate(self, attrs):
        """
        Authenticate the user using email and password.
        """

        email = attrs["email"].strip().lower()
        password = attrs["password"]

        try:
            user = User.objects.get(
                email__iexact=email
            )
        except User.DoesNotExist:
            raise serializers.ValidationError(
                {
                    "detail":
                    "Invalid email address or password."
                }
            )

        if not user.is_active:
            raise serializers.ValidationError(
                {
                    "detail":
                    "This account is inactive."
                }
            )

        if not user.email_verified:
            raise serializers.ValidationError(
                {
                    "email":
                    "Please verify your email before logging in."
                }
            )

        authenticated_user = authenticate(
            self.context.get("request"),
            username=user.username,
            password=password,
        )

        if authenticated_user is None:
            raise serializers.ValidationError(
                {
                    "detail":
                    "Invalid email address or password."
                }
            )

        refresh = RefreshToken.for_user(
            authenticated_user
        )

        # Add our custom JWT claims.
        refresh["username"] = authenticated_user.username
        refresh["role"] = authenticated_user.role
        refresh["email"] = authenticated_user.email

        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),

            "user": {
                "id": authenticated_user.id,
                "username": authenticated_user.username,
                "email": authenticated_user.email,
                "role": authenticated_user.role,
                "email_verified": (
                    authenticated_user.email_verified
                ),
            },
        }
class LogoutSerializer(serializers.Serializer):

#    Logout Serializer


    refresh = serializers.CharField()

    def validate(self, attrs):

        self.token = attrs["refresh"]

        return attrs

    def save(self, **kwargs):

        try:

            RefreshToken(self.token).blacklist()

        except Exception:

            raise serializers.ValidationError(
                "Invalid or expired refresh token."
            )

class UserProfileSerializer(serializers.ModelSerializer):

#    Logged-in User Profile Serializer


    class Meta:

        model = User

        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "phone",
            "role",
            "profile_image",
            "email_verified",
            "is_active",
            "date_joined",
        ]

        read_only_fields = fields

class ChangePasswordSerializer(serializers.Serializer):

#    Change Password Serializer

    old_password = serializers.CharField(
        write_only=True
    )

    new_password = serializers.CharField(
        write_only=True
    )

    confirm_password = serializers.CharField(
        write_only=True
    )

    def validate(self, attrs):

        user = self.context["request"].user

        if not user.check_password(attrs["old_password"]):
            raise serializers.ValidationError(
                {
                    "old_password": "Old password is incorrect."
                }
            )

        if attrs["new_password"] != attrs["confirm_password"]:
            raise serializers.ValidationError(
                {
                    "confirm_password": "Passwords do not match."
                }
            )

        validate_password(
            attrs["new_password"],
            user=user,
        )

        return attrs

    def save(self):

        user = self.context["request"].user

        user.set_password(
            self.validated_data["new_password"]
        )

        user.save()

        return user

class ResendVerificationEmailSerializer(serializers.Serializer):

    email = serializers.EmailField()

    def validate_email(self, value):

        try:
            user = User.objects.get(
                email__iexact=value
            )
        except User.DoesNotExist:
            raise serializers.ValidationError(
                "No account is associated with this email address."
            )

        if user.email_verified:
            raise serializers.ValidationError(
                "This email address is already verified."
            )

        self.user = user

        return value


class ForgotPasswordSerializer(serializers.Serializer):

    email = serializers.EmailField()

    def validate_email(self, value):

        try:
            user = User.objects.get(
                email__iexact=value
            )

        except User.DoesNotExist:
            raise serializers.ValidationError(
                "No account is associated with this email address."
            )

        if not user.is_active:
            raise serializers.ValidationError(
                "This account is inactive."
            )

        self.user = user

        return value

class ResetPasswordSerializer(serializers.Serializer):

    uid = serializers.CharField()
    token = serializers.CharField()

    new_password = serializers.CharField(
        write_only=True
    )

    confirm_password = serializers.CharField(
        write_only=True
    )

    def validate(self, attrs):

        # Check passwords match
        if attrs["new_password"] != attrs["confirm_password"]:
            raise serializers.ValidationError(
                {
                    "confirm_password":
                    "Passwords do not match."
                }
            )

        # Decode user ID
        try:
            uid = force_str(
                urlsafe_base64_decode(
                    attrs["uid"]
                )
            )

            user = User.objects.get(
                pk=uid
            )

        except (
            TypeError,
            ValueError,
            OverflowError,
            User.DoesNotExist,
        ):
            raise serializers.ValidationError(
                {
                    "uid":
                    "Invalid password reset link."
                }
            )

        # Validate reset token
        if not default_token_generator.check_token(
            user,
            attrs["token"],
        ):
            raise serializers.ValidationError(
                {
                    "token":
                    "Invalid or expired password reset link."
                }
            )

        # Validate password strength
        validate_password(
            attrs["new_password"],
            user=user,
        )

        self.user = user

        return attrs