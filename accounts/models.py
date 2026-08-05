from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Custom User model for the Employee Management System.
    Extends Django's built-in AbstractUser.
    """

    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        HR = "HR", "HR"
        EMPLOYEE = "EMPLOYEE", "Employee"

    phone = models.CharField(
        max_length=15,
        unique=True,
        blank=True,
        null=True,
        help_text="User phone number",
    )

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.EMPLOYEE,
        help_text="User role",
    )

    profile_image = models.ImageField(
        upload_to="profile_images/",
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.username