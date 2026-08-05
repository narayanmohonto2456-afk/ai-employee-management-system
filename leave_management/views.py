from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
)

from employees.models import Employee

from .forms import LeaveForm
from .models import Leave


class LeaveListView(LoginRequiredMixin, ListView):
    """
    Display leave applications.
    """

    model = Leave
    template_name = "leave_management/leave_list.html"
    context_object_name = "leaves"

    def get_queryset(self):
        user = self.request.user

        if user.role in ["ADMIN", "HR"]:
            return Leave.objects.select_related(
                "employee",
                "employee__user",
                "leave_type",
            )

        try:
            employee = Employee.objects.get(user=user)
            return Leave.objects.filter(
                employee=employee
            ).select_related(
                "leave_type"
            )
        except Employee.DoesNotExist:
            return Leave.objects.none()


class LeaveDetailView(
    LoginRequiredMixin,
    DetailView,
):
    """
    Display leave details.
    """

    model = Leave
    template_name = "leave_management/leave_detail.html"
    context_object_name = "leave"


class LeaveCreateView(
    LoginRequiredMixin,
    CreateView,
):
    """
    Employee applies for leave.
    """

    model = Leave
    form_class = LeaveForm
    template_name = "leave_management/leave_form.html"

    def form_valid(self, form):
        try:
            employee = Employee.objects.get(
                user=self.request.user
            )

            form.instance.employee = employee

            messages.success(
                self.request,
                "Leave request submitted successfully."
            )

            return super().form_valid(form)

        except Employee.DoesNotExist:
            messages.error(
                self.request,
                "Employee profile not found."
            )

            return redirect(
                "leave_management:leave_list"
            )


class LeaveUpdateView(
    LoginRequiredMixin,
    UpdateView,
):
    """
    Update leave request.
    """

    model = Leave
    form_class = LeaveForm
    template_name = "leave_management/leave_form.html"

    def form_valid(self, form):
        messages.success(
            self.request,
            "Leave updated successfully."
        )

        return super().form_valid(form)

@login_required
def approve_leave(request, pk):
    """
    Approve a leave request.
    """

    if request.user.role not in ["ADMIN", "HR"]:
        messages.error(
            request,
            "You are not authorized to approve leave."
        )
        return redirect("leave_management:leave_list")

    leave = get_object_or_404(Leave, pk=pk)

    leave.status = Leave.Status.APPROVED
    leave.save()

    messages.success(
        request,
        "Leave approved successfully."
    )

    return redirect("leave_management:leave_list")


@login_required
def reject_leave(request, pk):
    """
    Reject a leave request.
    """

    if request.user.role not in ["ADMIN", "HR"]:
        messages.error(
            request,
            "You are not authorized to reject leave."
        )
        return redirect("leave_management:leave_list")

    leave = get_object_or_404(Leave, pk=pk)

    leave.status = Leave.Status.REJECTED
    leave.save()

    messages.success(
        request,
        "Leave rejected successfully."
    )

    return redirect("leave_management:leave_list")