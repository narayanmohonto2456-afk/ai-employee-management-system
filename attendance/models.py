from django.db import models

from employees.models import Employee


class Attendance(models.Model):
    """
    Stores daily attendance records for employees.
    """

    class StatusChoices(models.TextChoices):
        PRESENT = "Present", "Present"
        ABSENT = "Absent", "Absent"
        LEAVE = "Leave", "Leave"
        HALF_DAY = "Half Day", "Half Day"

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name="attendance_records",
    )

    date = models.DateField()

    check_in = models.TimeField(
        blank=True,
        null=True,
    )

    check_out = models.TimeField(
        blank=True,
        null=True,
    )

    working_hours = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
    )

    status = models.CharField(
        max_length=20,
        choices=StatusChoices.choices,
        default=StatusChoices.PRESENT,
    )

    remarks = models.TextField(
    blank=True,
    help_text="Optional remarks about attendance",
)

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["-date", "-id"]
        verbose_name = "Attendance"
        verbose_name_plural = "Attendance Records"
        unique_together = ("employee", "date")

    def __str__(self):
        return f"{self.employee.employee_id} - {self.date} - {self.status}"