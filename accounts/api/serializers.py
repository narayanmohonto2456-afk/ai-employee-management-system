from django.contrib.auth import authenticate

from rest_framework import serializers

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from accounts.models import User
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model
from accounts.services.email_service import EmailService

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

    
class LoginSerializer(TokenObtainPairSerializer):

#    Custom Login Serializer

    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Custom Claims
        token["username"] = user.username
        token["role"] = user.role
        token["email"] = user.email

        return token

def validate(self, attrs):

    data = super().validate(attrs)

    if not self.user.email_verified:
        raise serializers.ValidationError(
            {
                "email": (
                    "Please verify your email "
                    "before logging in."
                )
            }
        )

    data["user"] = {
        "id": self.user.id,
        "username": self.user.username,
        "email": self.user.email,
        "role": self.user.role,
        "email_verified": self.user.email_verified,
    }

    return data

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