from django.db import models
from django.urls import reverse


class Department(models.Model):
    """
    Stores department information.
    """

    department_name = models.CharField(
        max_length=100,
        unique=True,
    )

    department_code = models.CharField(
        max_length=20,
        unique=True,
    )

    description = models.TextField(
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["department_name"]
        verbose_name = "Department"
        verbose_name_plural = "Departments"

    def __str__(self):
        return f"{self.department_name} ({self.department_code})"

    def get_absolute_url(self):
        return reverse(
            "departments:department_detail",
            kwargs={"pk": self.pk},
        )