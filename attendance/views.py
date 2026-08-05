from datetime import datetime
from decimal import Decimal

from django.shortcuts import redirect
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DetailView,
    DeleteView,
)

from .forms import AttendanceForm
from .models import Attendance
from django.views import View
from employees.models import Employee
from datetime import datetime
from decimal import Decimal
from django.utils import timezone
from django.http import JsonResponse


class AttendanceListView(LoginRequiredMixin, ListView):
    model = Attendance
    template_name = "attendance/attendance_list.html"
    context_object_name = "attendances"
    paginate_by = 10

    def get_queryset(self):

        queryset = Attendance.objects.select_related(
            "employee",
            "employee__user",
        )

    # Employee can only see their own attendance
        if self.request.user.role == "EMPLOYEE":
            queryset = queryset.filter(
                employee__user=self.request.user
            )

        employee = self.request.GET.get("employee")
        status = self.request.GET.get("status")
        date = self.request.GET.get("date")

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

        return queryset.order_by("-date", "-id")

class AttendanceCreateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    CreateView,
):
    permission_required = "attendance.add_attendance"
    model = Attendance
    form_class = AttendanceForm
    template_name = "attendance/attendance_form.html"
    success_url = reverse_lazy("attendance:attendance_list")

    def form_valid(self, form):
        messages.success(
            self.request,
            "Attendance record created successfully.",
        )
        return super().form_valid(form)


class AttendanceUpdateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UpdateView,
):
    permission_required = "attendance.change_attendance"
    model = Attendance
    form_class = AttendanceForm
    template_name = "attendance/attendance_form.html"
    success_url = reverse_lazy("attendance:attendance_list")

    def form_valid(self, form):
        messages.success(
            self.request,
            "Attendance record updated successfully.",
        )
        return super().form_valid(form)


class AttendanceDetailView(LoginRequiredMixin, DetailView):
    model = Attendance
    template_name = "attendance/attendance_detail.html"
    context_object_name = "attendance"


class AttendanceDeleteView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    DeleteView,
):
    permission_required = "attendance.delete_attendance"
    model = Attendance
    template_name = "attendance/attendance_confirm_delete.html"
    success_url = reverse_lazy("attendance:attendance_list")

    def form_valid(self, form):
        messages.success(
            self.request,
            "Attendance record deleted successfully.",
        )
        return super().form_valid(form)

class CheckInView(LoginRequiredMixin, View):

    def post(self, request):

        is_ajax = (
            request.headers.get("X-Requested-With")
            == "XMLHttpRequest"
        )

        try:

            employee = Employee.objects.get(
                user=request.user
            )

        except Employee.DoesNotExist:

            if is_ajax:

                return JsonResponse(
                    {
                        "success": False,
                        "message": "No employee profile is linked to your account."
                    },
                    status=404,
                )

            messages.error(
                request,
                "No employee profile is linked to your account."
            )

            return redirect("attendance:attendance_list")

        today = timezone.localdate()

        attendance = Attendance.objects.filter(
            employee=employee,
            date=today
        ).first()

        if attendance:

            if is_ajax:

                return JsonResponse(
                    {
                        "success": False,
                        "message": "You have already checked in today."
                    },
                    status=400,
                )

            messages.warning(
                request,
                "You have already checked in today."
            )

            return redirect("attendance:attendance_list")

        Attendance.objects.create(
            employee=employee,
            date=today,
            check_in=timezone.localtime().time(),
            status=Attendance.StatusChoices.PRESENT,
        )

        if is_ajax:

            return JsonResponse(
                {
                    "success": True,
                    "message": "Check In successful."
                }
            )

        messages.success(
            request,
            "Check In successful."
        )

        return redirect("attendance:attendance_list")

    
class CheckOutView(LoginRequiredMixin, View):

    def post(self, request):

        is_ajax = (
            request.headers.get("X-Requested-With")
            == "XMLHttpRequest"
        )

        try:

            employee = Employee.objects.get(
                user=request.user
            )

        except Employee.DoesNotExist:

            if is_ajax:

                return JsonResponse(
                    {
                        "success": False,
                        "message": "No employee profile is linked to your account."
                    },
                    status=404,
                )

            messages.error(
                request,
                "No employee profile is linked to your account."
            )

            return redirect("attendance:attendance_list")

        today = timezone.localdate()

        attendance = Attendance.objects.filter(
            employee=employee,
            date=today
        ).first()

        if not attendance:

            if is_ajax:

                return JsonResponse(
                    {
                        "success": False,
                        "message": "You must check in first."
                    },
                    status=400,
                )

            messages.error(
                request,
                "You must check in first."
            )

            return redirect("attendance:attendance_list")

        if attendance.check_out:

            if is_ajax:

                return JsonResponse(
                    {
                        "success": False,
                        "message": "You have already checked out."
                    },
                    status=400,
                )

            messages.warning(
                request,
                "You have already checked out."
            )

            return redirect("attendance:attendance_list")

        attendance.check_out = timezone.localtime().time()

        check_in_datetime = datetime.combine(
            today,
            attendance.check_in
        )

        check_out_datetime = datetime.combine(
            today,
            attendance.check_out
        )

        total_hours = (
            check_out_datetime - check_in_datetime
        ).total_seconds() / 3600

        attendance.working_hours = Decimal(
            round(total_hours, 2)
        )

        attendance.save()

        if is_ajax:

            return JsonResponse(
                {
                    "success": True,
                    "message": "Check Out successful."
                }
            )

        messages.success(
            request,
            "Check Out successful."
        )

        return redirect("attendance:attendance_list")