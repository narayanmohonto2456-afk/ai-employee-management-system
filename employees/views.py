from django.contrib import messages
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
)
from django.db.models import Q
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    View,
)

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from accounts.mixins import (
    HRRequiredMixin,
    NoCacheMixin,
)
from departments.models import Department

from .forms import EmployeeForm
from .models import Employee
from .serializers import EmployeeSerializer


# ============================================================
# EMPLOYEE WEB VIEWS
# ============================================================


class EmployeeListView(
    NoCacheMixin,
    LoginRequiredMixin,
    HRRequiredMixin,
    ListView,
):
    """
    Display employees with:

    - Search
    - Department filtering
    - Gender filtering
    - Pagination

    Only Admin and HR users can access this page.
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

        # ----------------------------------------------------
        # Search
        # ----------------------------------------------------

        if search:

            queryset = queryset.filter(
                Q(employee_id__icontains=search)
                | Q(user__first_name__icontains=search)
                | Q(user__last_name__icontains=search)
                | Q(user__username__icontains=search)
                | Q(user__email__icontains=search)
                | Q(designation__icontains=search)
            )

        # ----------------------------------------------------
        # Department filter
        # ----------------------------------------------------

        if department:

            queryset = queryset.filter(
                department_id=department
            )

        # ----------------------------------------------------
        # Gender filter
        # ----------------------------------------------------

        if gender:

            queryset = queryset.filter(
                gender=gender
            )

        return queryset.order_by("employee_id")

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context["departments"] = Department.objects.all()

        context["search_query"] = (
            self.request.GET.get("q", "")
        )

        context["selected_department"] = (
            self.request.GET.get(
                "department",
                "",
            )
        )

        context["selected_gender"] = (
            self.request.GET.get(
                "gender",
                "",
            )
        )

        return context


class EmployeeSearchAPIView(
    LoginRequiredMixin,
    HRRequiredMixin,
    View,
):
    """
    AJAX employee search endpoint.

    Only authenticated Admin and HR users
    can use this endpoint.
    """

    def get(self, request):

        queryset = Employee.objects.select_related(
            "user",
            "department",
        )

        search = request.GET.get("q")
        department = request.GET.get("department")
        gender = request.GET.get("gender")

        # ----------------------------------------------------
        # Search
        # ----------------------------------------------------

        if search:

            queryset = queryset.filter(
                Q(employee_id__icontains=search)
                | Q(user__first_name__icontains=search)
                | Q(user__last_name__icontains=search)
                | Q(user__username__icontains=search)
                | Q(user__email__icontains=search)
                | Q(designation__icontains=search)
            )

        # ----------------------------------------------------
        # Department filter
        # ----------------------------------------------------

        if department:

            queryset = queryset.filter(
                department_id=department
            )

        # ----------------------------------------------------
        # Gender filter
        # ----------------------------------------------------

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
    NoCacheMixin,
    LoginRequiredMixin,
    HRRequiredMixin,
    DetailView,
):
    """
    Display employee details.

    Only Admin and HR users can access
    employee management details.
    """

    model = Employee
    template_name = "employees/employee_detail.html"
    context_object_name = "employee"


class EmployeeCreateView(
    NoCacheMixin,
    LoginRequiredMixin,
    HRRequiredMixin,
    PermissionRequiredMixin,
    CreateView,
):
    """
    Create a new employee.

    Requires:
        employees.add_employee

    Only Admin and HR users are allowed.
    """

    model = Employee
    form_class = EmployeeForm
    template_name = "employees/employee_form.html"

    permission_required = "employees.add_employee"

    def form_valid(self, form):

        messages.success(
            self.request,
            "Employee created successfully.",
        )

        return super().form_valid(form)


class EmployeeUpdateView(
    NoCacheMixin,
    LoginRequiredMixin,
    HRRequiredMixin,
    PermissionRequiredMixin,
    UpdateView,
):
    """
    Update an existing employee.

    Requires:
        employees.change_employee
    """

    model = Employee
    form_class = EmployeeForm
    template_name = "employees/employee_form.html"

    permission_required = "employees.change_employee"

    def form_valid(self, form):

        messages.success(
            self.request,
            "Employee updated successfully.",
        )

        return super().form_valid(form)


class EmployeeDeleteView(
    NoCacheMixin,
    LoginRequiredMixin,
    HRRequiredMixin,
    PermissionRequiredMixin,
    DeleteView,
):
    """
    Delete an employee.

    Requires:
        employees.delete_employee
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
            "Employee deleted successfully.",
        )

        return super().form_valid(form)


# ============================================================
# EMPLOYEE REST API
# ============================================================


class EmployeeListCreateAPIView(
    generics.ListCreateAPIView
):
    """
    Employee REST API.

    GET:
        Authenticated users can view employees.

    POST:
        Only Admin/HR users with the appropriate
        Django permission should be able to create employees.
    """

    queryset = Employee.objects.select_related(
        "user",
        "department",
    )

    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated]


class EmployeeDetailAPIView(
    generics.RetrieveUpdateDestroyAPIView
):
    """
    Employee REST API detail endpoint.

    GET:
        Authenticated users can view an employee.

    PUT/PATCH:
        Requires appropriate permissions.

    DELETE:
        Requires appropriate permissions.
    """

    queryset = Employee.objects.select_related(
        "user",
        "department",
    )

    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated]