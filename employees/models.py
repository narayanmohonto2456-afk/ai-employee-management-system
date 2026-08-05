from django.db import models
from django.urls import reverse
from django.conf import settings

from departments.models import Department


class Employee(models.Model):
    """
    Employee Profile Model
    """

    GENDER_CHOICES = (
        ("Male", "Male"),
        ("Female", "Female"),
        ("Other", "Other"),
    )

    employee_id = models.CharField(
        max_length=20,
        unique=True
    )

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="employee_profile"
    )

    department = models.ForeignKey(
        Department,
        on_delete=models.PROTECT,
        related_name="employees"
    )

    designation = models.CharField(
        max_length=100
    )

    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES
    )

    date_of_birth = models.DateField()

    joining_date = models.DateField()

    address = models.TextField()

    city = models.CharField(
        max_length=100
    )

    state = models.CharField(
        max_length=100
    )

    country = models.CharField(
        max_length=100
    )

    profile_picture = models.ImageField(
        upload_to="employees/",
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["employee_id"]
        verbose_name = "Employee"
        verbose_name_plural = "Employees"

    def __str__(self):
        return f"{self.employee_id} - {self.user.get_full_name()}"

    def get_absolute_url(self):
        return reverse(
            "employees:employee_detail",
            kwargs={"pk": self.pk},
        )