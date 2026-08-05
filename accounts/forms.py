from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.forms import PasswordChangeForm

from .models import User


class UserRegistrationForm(UserCreationForm):

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

        # Every newly registered user becomes an Employee
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
    User Login Form
    """

    username = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control"}
        )
    )

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control"}
        )
    )


class UserUpdateForm(forms.ModelForm):
    """
    Update User Profile
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