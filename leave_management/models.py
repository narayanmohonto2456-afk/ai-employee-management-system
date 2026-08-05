from django.db import models
from django.urls import reverse

from employees.models import Employee


class LeaveType(models.Model):
    """
    Different types of leave.
    """

    name = models.CharField(
        max_length=100,
        unique=True,
    )

    description = models.TextField(
        blank=True,
    )

    def __str__(self):
        return self.name


class Leave(models.Model):
    """
    Employee leave application.
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
        on_delete=models.CASCADE,
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

    def __str__(self):
        return (
            f"{self.employee} - "
            f"{self.leave_type}"
        )

    def get_absolute_url(self):
        return reverse(
            "leave_management:leave_detail",
            kwargs={"pk": self.pk},
        )