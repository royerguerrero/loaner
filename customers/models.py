"""Customers models"""

# Django
from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class Customer(models.Model):
    """Customers model"""
    class Status(models.IntegerChoices):
        """Customer status"""
        ACTIVE = 1
        INACTIVE = 2

    score = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.PositiveSmallIntegerField(
        choices=Status.choices,
        default=Status.ACTIVE
    )
    preapproved_at = models.DateTimeField()
    external_id = models.CharField(max_length=60, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.external_id}'


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
