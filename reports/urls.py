from django.urls import path
from .views import (
    AttendanceReportView,
    AttendanceExcelExportView,
    AttendancePDFExportView,
)

app_name = "reports"

urlpatterns = [
    path(
        "attendance/",
        AttendanceReportView.as_view(),
        name="attendance_report",
    ),
    path(
    "attendance/excel/",
    AttendanceExcelExportView.as_view(),
    name="attendance_excel"),
path(
    "attendance/pdf/",
    AttendancePDFExportView.as_view(),
    name="attendance_pdf",
),
]