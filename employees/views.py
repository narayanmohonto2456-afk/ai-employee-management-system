from django.contrib import messages
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
)
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    View,
)

from accounts.mixins import HRRequiredMixin
from departments.models import Department

from .forms import EmployeeForm
from .models import Employee
from django.http import JsonResponse
from django.template.loader import render_to_string


class EmployeeListView(
    LoginRequiredMixin,
    HRRequiredMixin,
    ListView,
):
    """
    Employee List with Search, Filtering and Pagination.
    """

    model = Employee
    template_name = "employees/employee_list.html"
    context_object_name = "employees"
    paginate_by = 10

    def get_queryset(self):
        queryset = Employee.objects.select_related(
            "user",
            "department",
        )

        search = self.request.GET.get("q")
        department = self.request.GET.get("department")
        gender = self.request.GET.get("gender")

        if search:
            queryset = queryset.filter(
                Q(employee_id__icontains=search)
                | Q(user__first_name__icontains=search)
                | Q(user__last_name__icontains=search)
                | Q(user__username__icontains=search)
                | Q(designation__icontains=search)
            )

        if department:
            queryset = queryset.filter(
                department_id=department
            )

        if gender:
            queryset = queryset.filter(
                gender=gender
            )

        return queryset.order_by("employee_id")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["departments"] = Department.objects.all()
        context["search_query"] = self.request.GET.get("q", "")
        context["selected_department"] = self.request.GET.get(
            "department",
            "",
        )
        context["selected_gender"] = self.request.GET.get(
            "gender",
            "",
        )

        return context

class EmployeeSearchAPIView(
    LoginRequiredMixin,
    HRRequiredMixin,
    View,
):

    def get(self, request):

        queryset = Employee.objects.select_related(
            "user",
            "department",
        )

        search = request.GET.get("q")

        department = request.GET.get("department")

        gender = request.GET.get("gender")

        if search:

            queryset = queryset.filter(

                Q(employee_id__icontains=search)

                | Q(user__first_name__icontains=search)

                | Q(user__last_name__icontains=search)

                | Q(user__username__icontains=search)

                | Q(designation__icontains=search)

            )

        if department:

            queryset = queryset.filter(
                department_id=department
            )

        if gender:

            queryset = queryset.filter(
                gender=gender
            )

        html = render_to_string(

            "employees/partials/employee_table.html",

            {
                "employees": queryset.order_by(
                    "employee_id"
                )
            },

            request=request,

        )

        return JsonResponse(
            {
                "html": html
            }
        )


class EmployeeDetailView(
    LoginRequiredMixin,
    HRRequiredMixin,
    DetailView,
):
    """
    Display employee details.
    """

    model = Employee
    template_name = "employees/employee_detail.html"
    context_object_name = "employee"


class EmployeeCreateView(
    LoginRequiredMixin,
    HRRequiredMixin,
    PermissionRequiredMixin,
    CreateView,
):
    """
    Create a new employee.
    """

    model = Employee
    form_class = EmployeeForm
    template_name = "employees/employee_form.html"

    permission_required = "employees.add_employee"

    def form_valid(self, form):
        messages.success(
            self.request,
            "Employee created successfully."
        )
        return super().form_valid(form)


class EmployeeUpdateView(
    LoginRequiredMixin,
    HRRequiredMixin,
    PermissionRequiredMixin,
    UpdateView,
):
    """
    Update employee.
    """

    model = Employee
    form_class = EmployeeForm
    template_name = "employees/employee_form.html"

    permission_required = "employees.change_employee"

    def form_valid(self, form):
        messages.success(
            self.request,
            "Employee updated successfully."
        )
        return super().form_valid(form)


class EmployeeDeleteView(
    LoginRequiredMixin,
    HRRequiredMixin,
    PermissionRequiredMixin,
    DeleteView,
):
    """
    Delete employee.
    """

    model = Employee
    template_name = "employees/employee_confirm_delete.html"
    context_object_name = "employee"

    permission_required = "employees.delete_employee"

    success_url = reverse_lazy(
        "employees:employee_list"
    )

    def form_valid(self, form):
        messages.success(
            self.request,
            "Employee deleted successfully."
        )
        return super().form_valid(form)