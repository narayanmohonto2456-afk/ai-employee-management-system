from datetime import datetime
from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
)
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from accounts.mixins import HRRequiredMixin, NoCacheMixin
from employees.models import Employee

from .forms import AttendanceForm
from .models import Attendance


# ============================================================
# ATTENDANCE LIST
# ============================================================


class AttendanceListView(
    NoCacheMixin,
    LoginRequiredMixin,
    ListView,
):
    """
    Display attendance records.

    ADMIN / HR:
        Can view all attendance records.

    EMPLOYEE:
        Can only view their own attendance records.

    Supports:
        - Employee search
        - Status filtering
        - Date filtering
        - Pagination
    """

    model = Attendance
    template_name = "attendance/attendance_list.html"
    context_object_name = "attendances"
    paginate_by = 10

    def get_queryset(self):

        queryset = Attendance.objects.select_related(
            "employee",
            "employee__user",
            "employee__department",
        )

        user = self.request.user

        # ----------------------------------------------------
        # Employee can only see own attendance
        # ----------------------------------------------------

        if getattr(user, "role", None) == "EMPLOYEE":

            queryset = queryset.filter(
                employee__user=user
            )

        # ----------------------------------------------------
        # Search / filters
        # ----------------------------------------------------

        employee = self.request.GET.get(
            "employee",
            "",
        ).strip()

        status = self.request.GET.get(
            "status",
            "",
        ).strip()

        date = self.request.GET.get(
            "date",
            "",
        ).strip()

        if employee:

            queryset = queryset.filter(
                employee__employee_id__icontains=employee
            )

        if status:

            queryset = queryset.filter(
                status=status
            )

        if date:

            queryset = queryset.filter(
                date=date
            )

        return queryset.order_by(
            "-date",
            "-id",
        )


# ============================================================
# CREATE ATTENDANCE
# ============================================================


class AttendanceCreateView(
    NoCacheMixin,
    LoginRequiredMixin,
    HRRequiredMixin,
    PermissionRequiredMixin,
    CreateView,
):
    """
    Create an attendance record.

    Only ADMIN / HR users with the required
    Django permission can create attendance.
    """

    model = Attendance
    form_class = AttendanceForm
    template_name = "attendance/attendance_form.html"

    permission_required = "attendance.add_attendance"

    success_url = reverse_lazy(
        "attendance:attendance_list"
    )

    def form_valid(self, form):

        messages.success(
            self.request,
            "Attendance record created successfully.",
        )

        return super().form_valid(form)


# ============================================================
# UPDATE ATTENDANCE
# ============================================================


class AttendanceUpdateView(
    NoCacheMixin,
    LoginRequiredMixin,
    HRRequiredMixin,
    PermissionRequiredMixin,
    UpdateView,
):
    """
    Update an attendance record.

    Only ADMIN / HR users with the required
    Django permission can update attendance.
    """

    model = Attendance
    form_class = AttendanceForm
    template_name = "attendance/attendance_form.html"

    permission_required = "attendance.change_attendance"

    success_url = reverse_lazy(
        "attendance:attendance_list"
    )

    def form_valid(self, form):

        messages.success(
            self.request,
            "Attendance record updated successfully.",
        )

        return super().form_valid(form)


# ============================================================
# ATTENDANCE DETAIL
# ============================================================


class AttendanceDetailView(
    NoCacheMixin,
    LoginRequiredMixin,
    DetailView,
):
    """
    Display a single attendance record.

    ADMIN / HR:
        Can view any attendance record.

    EMPLOYEE:
        Can only view their own attendance record.
    """

    model = Attendance
    template_name = "attendance/attendance_detail.html"
    context_object_name = "attendance"

    def get_queryset(self):

        queryset = Attendance.objects.select_related(
            "employee",
            "employee__user",
            "employee__department",
        )

        user = self.request.user

        if getattr(user, "role", None) == "EMPLOYEE":

            queryset = queryset.filter(
                employee__user=user
            )

        return queryset


# ============================================================
# DELETE ATTENDANCE
# ============================================================


class AttendanceDeleteView(
    NoCacheMixin,
    LoginRequiredMixin,
    HRRequiredMixin,
    PermissionRequiredMixin,
    DeleteView,
):
    """
    Delete an attendance record.

    Only ADMIN / HR users with the required
    Django permission can delete attendance.
    """

    model = Attendance
    template_name = "attendance/attendance_confirm_delete.html"
    context_object_name = "attendance"

    permission_required = "attendance.delete_attendance"

    success_url = reverse_lazy(
        "attendance:attendance_list"
    )

    def form_valid(self, form):

        messages.success(
            self.request,
            "Attendance record deleted successfully.",
        )

        return super().form_valid(form)


# ============================================================
# EMPLOYEE CHECK-IN
# ============================================================


class CheckInView(
    LoginRequiredMixin,
    View,
):
    """
    Allow an authenticated employee to check in.

    Rules:

        1. User must be authenticated.
        2. User must have an Employee profile.
        3. Only one check-in per day.
        4. Attendance status becomes PRESENT.
    """

    def post(self, request):

        is_ajax = (
            request.headers.get("X-Requested-With")
            == "XMLHttpRequest"
        )

        # ----------------------------------------------------
        # Find employee profile
        # ----------------------------------------------------

        try:

            employee = Employee.objects.get(
                user=request.user
            )

        except Employee.DoesNotExist:

            response = {
                "success": False,
                "message": (
                    "No employee profile is linked "
                    "to your account."
                ),
            }

            if is_ajax:

                return JsonResponse(
                    response,
                    status=404,
                )

            messages.error(
                request,
                response["message"],
            )

            return redirect(
                "attendance:attendance_list"
            )

        # ----------------------------------------------------
        # Today's date
        # ----------------------------------------------------

        today = timezone.localdate()

        # ----------------------------------------------------
        # Check whether attendance already exists
        # ----------------------------------------------------

        attendance = Attendance.objects.filter(
            employee=employee,
            date=today,
        ).first()

        if attendance:

            response = {
                "success": False,
                "message": (
                    "You have already checked in today."
                ),
            }

            if is_ajax:

                return JsonResponse(
                    response,
                    status=400,
                )

            messages.warning(
                request,
                response["message"],
            )

            return redirect(
                "attendance:attendance_list"
            )

        # ----------------------------------------------------
        # Create attendance
        # ----------------------------------------------------

        Attendance.objects.create(
            employee=employee,
            date=today,
            check_in=timezone.localtime().time(),
            status=Attendance.StatusChoices.PRESENT,
        )

        response = {
            "success": True,
            "message": "Check In successful.",
        }

        if is_ajax:

            return JsonResponse(
                response,
                status=200,
            )

        messages.success(
            request,
            response["message"],
        )

        return redirect(
            "attendance:attendance_list"
        )


# ============================================================
# EMPLOYEE CHECK-OUT
# ============================================================


class CheckOutView(
    LoginRequiredMixin,
    View,
):
    """
    Allow an authenticated employee to check out.

    Rules:

        1. User must have an Employee profile.
        2. Employee must check in first.
        3. Employee can check out only once.
        4. Working hours are calculated automatically.
    """

    def post(self, request):

        is_ajax = (
            request.headers.get("X-Requested-With")
            == "XMLHttpRequest"
        )

        # ----------------------------------------------------
        # Find employee profile
        # ----------------------------------------------------

        try:

            employee = Employee.objects.get(
                user=request.user
            )

        except Employee.DoesNotExist:

            response = {
                "success": False,
                "message": (
                    "No employee profile is linked "
                    "to your account."
                ),
            }

            if is_ajax:

                return JsonResponse(
                    response,
                    status=404,
                )

            messages.error(
                request,
                response["message"],
            )

            return redirect(
                "attendance:attendance_list"
            )

        # ----------------------------------------------------
        # Today's attendance
        # ----------------------------------------------------

        today = timezone.localdate()

        attendance = Attendance.objects.filter(
            employee=employee,
            date=today,
        ).first()

        # ----------------------------------------------------
        # Employee has not checked in
        # ----------------------------------------------------

        if not attendance:

            response = {
                "success": False,
                "message": "You must check in first.",
            }

            if is_ajax:

                return JsonResponse(
                    response,
                    status=400,
                )

            messages.error(
                request,
                response["message"],
            )

            return redirect(
                "attendance:attendance_list"
            )

        # ----------------------------------------------------
        # Already checked out
        # ----------------------------------------------------

        if attendance.check_out:

            response = {
                "success": False,
                "message": (
                    "You have already checked out."
                ),
            }

            if is_ajax:

                return JsonResponse(
                    response,
                    status=400,
                )

            messages.warning(
                request,
                response["message"],
            )

            return redirect(
                "attendance:attendance_list"
            )

        # ----------------------------------------------------
        # Set check-out time
        # ----------------------------------------------------

        check_out = timezone.localtime().time()

        attendance.check_out = check_out

        # ----------------------------------------------------
        # Calculate working hours
        # ----------------------------------------------------

        check_in_datetime = datetime.combine(
            today,
            attendance.check_in,
        )

        check_out_datetime = datetime.combine(
            today,
            check_out,
        )

        total_seconds = (
            check_out_datetime
            - check_in_datetime
        ).total_seconds()

        total_hours = total_seconds / 3600

        attendance.working_hours = Decimal(
            str(round(total_hours, 2))
        )

        attendance.save(
            update_fields=[
                "check_out",
                "working_hours",
                "updated_at",
            ]
        )

        # ----------------------------------------------------
        # Response
        # ----------------------------------------------------

        response = {
            "success": True,
            "message": "Check Out successful.",
            "working_hours": float(
                attendance.working_hours
            ),
        }

        if is_ajax:

            return JsonResponse(
                response,
                status=200,
            )

        messages.success(
            request,
            (
                "Check Out successful. "
                f"Working hours: "
                f"{attendance.working_hours}"
            ),
        )

        return redirect(
            "attendance:attendance_list"
        )