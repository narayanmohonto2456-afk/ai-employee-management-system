from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.mixins import HRRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView

from .forms import (
    UserRegistrationForm,
    CustomLoginForm,
    UserUpdateForm,CustomPasswordChangeForm,
)
from .models import User


class RegisterView(CreateView):
    """
    Register a new user.
    """

    model = User
    form_class = UserRegistrationForm
    template_name = "accounts/register.html"
    success_url = reverse_lazy("accounts:login")

    def form_valid(self, form):
        user = form.save()
        messages.success(
            self.request,
            "Registration completed successfully."
        )
        login(self.request, user)
        return redirect("accounts:profile")


class CustomLoginView(LoginView):
    """
    User Login
    """

    authentication_form = CustomLoginForm
    template_name = "accounts/login.html"

    def get_success_url(self):
        return reverse_lazy("accounts:profile")


class CustomLogoutView(LogoutView):
    """
    Logout user.
    """

    next_page = reverse_lazy("accounts:login")


class ProfileView(LoginRequiredMixin, DetailView):
    """
    Display logged-in user's profile.
    """

    model = User
    template_name = "accounts/profile.html"
    context_object_name = "user_obj"

    def get_object(self):
        return self.request.user


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """
    Update user profile.
    """

    model = User
    form_class = UserUpdateForm
    template_name = "accounts/profile_update.html"

    def get_object(self):
        return self.request.user

    def get_success_url(self):
        messages.success(
            self.request,
            "Profile updated successfully."
        )
        return reverse_lazy("accounts:profile")
    
class CustomPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    """
    Allow logged-in users to change their password.
    """

    form_class = CustomPasswordChangeForm
    template_name = "accounts/change_password.html"
    success_url = reverse_lazy("accounts:profile")

    def form_valid(self, form):
        messages.success(
            self.request,
            "Your password has been changed successfully."
        )
        return super().form_valid(form)
   
   
    def get_success_url(self):
        return reverse_lazy("dashboard:dashboard")