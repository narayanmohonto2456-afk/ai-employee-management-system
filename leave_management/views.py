from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
)

from employees.models import Employee

from .forms import LeaveForm
from .models import Leave


# ============================================================
# LEAVE LIST
# ============================================================


class LeaveListView(
    LoginRequiredMixin,
    ListView,
):
    """
    Display leave applications.

    Admin and HR:
        Can see all leave applications.

    Employee:
        Can see only their own leave applications.
    """

    model = Leave
    template_name = "leave_management/leave_list.html"
    context_object_name = "leaves"

    def get_queryset(self):

        user = self.request.user

        queryset = Leave.objects.select_related(
            "employee",
            "employee__user",
            "leave_type",
        )

        # ----------------------------------------------------
        # Admin / HR
        # ----------------------------------------------------

        if user.role in ["ADMIN", "HR"]:
            return queryset

        # ----------------------------------------------------
        # Employee
        # ----------------------------------------------------

        try:

            employee = Employee.objects.get(
                user=user
            )

        except Employee.DoesNotExist:

            return Leave.objects.none()

        return queryset.filter(
            employee=employee
        )


# ============================================================
# LEAVE DETAIL
# ============================================================


class LeaveDetailView(
    LoginRequiredMixin,
    DetailView,
):
    """
    Display leave details.

    Admin and HR:
        Can view any leave.

    Employee:
        Can view only their own leave.
    """

    model = Leave
    template_name = "leave_management/leave_detail.html"
    context_object_name = "leave"

    def get_queryset(self):

        user = self.request.user

        queryset = Leave.objects.select_related(
            "employee",
            "employee__user",
            "leave_type",
        )

        # Admin / HR can view everything.
        if user.role in ["ADMIN", "HR"]:
            return queryset

        # Employee can view only their own records.
        try:

            employee = Employee.objects.get(
                user=user
            )

        except Employee.DoesNotExist:

            return Leave.objects.none()

        return queryset.filter(
            employee=employee
        )


# ============================================================
# APPLY FOR LEAVE
# ============================================================


class LeaveCreateView(
    LoginRequiredMixin,
    CreateView,
):
    """
    Employee applies for leave.

    The employee is automatically taken
    from the logged-in user's Employee profile.
    """

    model = Leave
    form_class = LeaveForm
    template_name = "leave_management/leave_form.html"

    def form_valid(self, form):

        try:

            employee = Employee.objects.get(
                user=self.request.user
            )

        except Employee.DoesNotExist:

            messages.error(
                self.request,
                "Employee profile not found.",
            )

            return redirect(
                "leave_management:leave_list"
            )

        form.instance.employee = employee

        # Always create a new leave as Pending.
        form.instance.status = Leave.Status.PENDING

        messages.success(
            self.request,
            "Leave request submitted successfully.",
        )

        return super().form_valid(form)


# ============================================================
# UPDATE LEAVE
# ============================================================


class LeaveUpdateView(
    LoginRequiredMixin,
    UpdateView,
):
    """
    Update a leave request.

    Admin / HR:
        Can update any leave.

    Employee:
        Can update only their own leave.

    Approved or rejected leaves cannot be
    modified by employees.
    """

    model = Leave
    form_class = LeaveForm
    template_name = "leave_management/leave_form.html"

    def get_queryset(self):

        user = self.request.user

        queryset = Leave.objects.select_related(
            "employee",
            "employee__user",
            "leave_type",
        )

        # Admin / HR
        if user.role in ["ADMIN", "HR"]:
            return queryset

        # Employee
        try:

            employee = Employee.objects.get(
                user=user
            )

        except Employee.DoesNotExist:

            return Leave.objects.none()

        return queryset.filter(
            employee=employee
        )

    def dispatch(self, request, *args, **kwargs):

        leave = self.get_object()

        # Employees should not edit processed leaves.
        if (
            request.user.role == "EMPLOYEE"
            and leave.status != Leave.Status.PENDING
        ):

            messages.error(
                request,
                "Processed leave requests cannot be modified.",
            )

            return redirect(
                "leave_management:leave_detail",
                pk=leave.pk,
            )

        return super().dispatch(
            request,
            *args,
            **kwargs,
        )

    def form_valid(self, form):

        # If an employee edits their pending leave,
        # keep it pending.
        if self.request.user.role == "EMPLOYEE":

            form.instance.status = Leave.Status.PENDING

        messages.success(
            self.request,
            "Leave updated successfully.",
        )

        return super().form_valid(form)


# ============================================================
# APPROVE LEAVE
# ============================================================


@login_required
def approve_leave(request, pk):
    """
    Approve a leave request.

    Only Admin and HR users can approve leave.

    Approval must use POST.
    """

    if request.user.role not in ["ADMIN", "HR"]:

        messages.error(
            request,
            "You are not authorized to approve leave.",
        )

        return redirect(
            "leave_management:leave_list"
        )

    if request.method != "POST":

        messages.error(
            request,
            "Invalid request method.",
        )

        return redirect(
            "leave_management:leave_list"
        )

    leave = get_object_or_404(
        Leave,
        pk=pk,
    )

    if leave.status != Leave.Status.PENDING:

        messages.warning(
            request,
            "This leave request has already been processed.",
        )

        return redirect(
            "leave_management:leave_list"
        )

    leave.status = Leave.Status.APPROVED

    leave.save(
        update_fields=[
            "status",
            "updated_at",
        ]
    )

    messages.success(
        request,
        "Leave approved successfully.",
    )

    return redirect(
        "leave_management:leave_list"
    )


# ============================================================
# REJECT LEAVE
# ============================================================


@login_required
def reject_leave(request, pk):
    """
    Reject a leave request.

    Only Admin and HR users can reject leave.

    Rejection must use POST.
    """

    if request.user.role not in ["ADMIN", "HR"]:

        messages.error(
            request,
            "You are not authorized to reject leave.",
        )

        return redirect(
            "leave_management:leave_list"
        )

    if request.method != "POST":

        messages.error(
            request,
            "Invalid request method.",
        )

        return redirect(
            "leave_management:leave_list"
        )

    leave = get_object_or_404(
        Leave,
        pk=pk,
    )

    if leave.status != Leave.Status.PENDING:

        messages.warning(
            request,
            "This leave request has already been processed.",
        )

        return redirect(
            "leave_management:leave_list"
        )

    leave.status = Leave.Status.REJECTED

    leave.save(
        update_fields=[
            "status",
            "updated_at",
        ]
    )

    messages.success(
        request,
        "Leave rejected successfully.",
    )

    return redirect(
        "leave_management:leave_list"
    )