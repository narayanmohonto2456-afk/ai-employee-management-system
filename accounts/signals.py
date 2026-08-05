from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group

from .models import User


@receiver(post_save, sender=User)
def assign_employee_group(sender, instance, created, **kwargs):
    """
    Automatically assign every newly created user
    to the Employee group.
    """
    if created:
        employee_group, _ = Group.objects.get_or_create(
            name="Employee"
        )
        instance.groups.add(employee_group)