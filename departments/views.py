from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)

from .forms import DepartmentForm
from .models import Department
from django.db.models import Q

class DepartmentListView(LoginRequiredMixin, ListView):
    """
    Display all departments with search functionality.
    """

    model = Department
    template_name = "departments/department_list.html"
    context_object_name = "departments"
    paginate_by = 10

    def get_queryset(self):
        queryset = Department.objects.all().order_by("department_name")

        search = self.request.GET.get("search")

        if search:
            queryset = queryset.filter(
                Q(department_name__icontains=search) |
                Q(department_code__icontains=search) |
                Q(description__icontains=search)
            )

        return queryset

class DepartmentDetailView(LoginRequiredMixin, DetailView):
    """
    Display one department.
    """

    model = Department
    template_name = "departments/department_detail.html"
    context_object_name = "department"

class DepartmentCreateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    CreateView,
):
    """
    Create a department.
    """

    model = Department
    form_class = DepartmentForm
    template_name = "departments/department_form.html"
    permission_required = "departments.add_department"

    def form_valid(self, form):
        messages.success(
            self.request,
            "Department created successfully."
        )
        return super().form_valid(form)
class DepartmentUpdateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UpdateView,
):
    """
    Update a department.
    """

    model = Department
    form_class = DepartmentForm
    template_name = "departments/department_form.html"
    permission_required = "departments.change_department"

    def form_valid(self, form):
        messages.success(
            self.request,
            "Department updated successfully."
        )
        return super().form_valid(form)
class DepartmentDeleteView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    DeleteView,
):
    """
    Delete a department.
    """

    model = Department
    context_object_name = "department"
    template_name = "departments/department_confirm_delete.html"
    permission_required = "departments.delete_department"
    success_url = reverse_lazy("departments:department_list")

    def form_valid(self, form):
        messages.success(
            self.request,
            "Department deleted successfully."
        )
        return super().form_valid(form)
