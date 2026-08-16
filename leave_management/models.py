from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse

from employees.models import Employee


class LeaveType(models.Model):
    """
    Stores different types of leave.
    """

    name = models.CharField(
        max_length=100,
        unique=True,
    )

    description = models.TextField(
        blank=True,
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Leave Type"
        verbose_name_plural = "Leave Types"

    def __str__(self):
        return self.name


class Leave(models.Model):
    """
    Stores employee leave applications.
    """

    class Status(models.TextChoices):
        PENDING = "Pending", "Pending"
        APPROVED = "Approved", "Approved"
        REJECTED = "Rejected", "Rejected"

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name="leaves",
    )

    leave_type = models.ForeignKey(
        LeaveType,
        on_delete=models.PROTECT,
        related_name="leaves",
    )

    start_date = models.DateField()

    end_date = models.DateField()

    reason = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )

    applied_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["-applied_at"]
        verbose_name = "Leave"
        verbose_name_plural = "Leaves"

    def clean(self):
        """
        Validate leave dates.
        """

        if (
            self.start_date
            and self.end_date
            and self.end_date < self.start_date
        ):
            raise ValidationError(
                {
                    "end_date": (
                        "End date cannot be earlier "
                        "than start date."
                    )
                }
            )

    def __str__(self):
        return (
            f"{self.employee.employee_id} - "
            f"{self.leave_type.name} - "
            f"{self.status}"
        )

    def get_absolute_url(self):
        return reverse(
            "leave_management:leave_detail",
            kwargs={"pk": self.pk},
        )