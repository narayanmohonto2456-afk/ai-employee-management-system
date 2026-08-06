
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from .views import dashboard

urlpatterns = [
    path("", include("dashboard.urls")),
    path('admin/', admin.site.urls),

    # Each app's own urls.py gets included here as we build it, e.g.:
    path('accounts/', include('accounts.urls')),      # Module 3+
    path('departments/', include('departments.urls')),  # Module 6
    path('api/', include('api.urls')),                 # Module 12+
    path('attendance/', include('attendance.urls')),
    path('employees/' , include('employees.urls')),
    path('leave-management/', include('leave_management.urls')),
    path("reports/", include("reports.urls")),
    path("api/auth/",include("accounts.api.urls"),),
]

if settings.DEBUG:
    # Only Django's dev server needs to serve /media/ itself — in production
    # nginx/whatever web server handles this directly. See the deployment module.
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
