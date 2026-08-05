from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def dashboard(request):
    """
    Dashboard Home Page
    """

    context = {
        "total_employees": 0,
        "total_departments": 0,
        "present_today": 0,
        "employees_on_leave": 0,
    }

    return render(
        request,
        "dashboard.html",
        context,
    )