from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import (
    UserCreationForm,
    AuthenticationForm,
    PasswordChangeForm,
)

from .models import User


class UserRegistrationForm(UserCreationForm):
    """
    User registration form.
    """

    class Meta:
        model = User

        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "phone",
            "profile_image",
        )

    def save(self, commit=True):
        user = super().save(commit=False)

        # Every newly registered user becomes an Employee.
        user.role = User.Role.EMPLOYEE

        if commit:
            user.save()

        return user

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"


class CustomLoginForm(AuthenticationForm):
    """
    Authenticate users using email address and password.
    """

    username = forms.EmailField(
        label="Email Address",
        required=True,
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter your email address",
                "autocomplete": "email",
            }
        ),
    )

    password = forms.CharField(
        label="Password",
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter your password",
                "autocomplete": "current-password",
            }
        ),
    )

    def clean(self):
        """
        Authenticate the user using email address and password.
        """

        # IMPORTANT:
        # Do NOT call super().clean() here because Django's
        # AuthenticationForm tries to authenticate using username.
        cleaned_data = self.cleaned_data

        email = cleaned_data.get("username")
        password = cleaned_data.get("password")

        if not email or not password:
            raise forms.ValidationError(
                "Please enter your email address and password."
            )

        email = email.strip().lower()

        try:
            user = User.objects.get(
                email__iexact=email
            )
        except User.DoesNotExist:
            raise forms.ValidationError(
                "Invalid email address or password."
            )

        if not user.check_password(password):
            raise forms.ValidationError(
                "Invalid email address or password."
            )

        # Check whether the account is allowed to log in.
        self.confirm_login_allowed(user)

        # AuthenticationForm's login() process uses user_cache.
        self.user_cache = user

        return cleaned_data


class UserUpdateForm(forms.ModelForm):
    """
    Update User Profile.
    """

    class Meta:
        model = User

        fields = (
            "first_name",
            "last_name",
            "email",
            "phone",
            "profile_image",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({
                "class": "form-control"
            })


class ProfileImageForm(forms.ModelForm):
    """
    Update only profile image.
    """

    class Meta:
        model = User
        fields = ("profile_image",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["profile_image"].widget.attrs.update({
            "class": "form-control"
        })


class CustomPasswordChangeForm(PasswordChangeForm):
    """
    Form used by authenticated users to change their password.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({
                "class": "form-control"
            })