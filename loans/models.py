"""Loans models"""

# Django
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from django.utils import timezone
from django.core.exceptions import ValidationError

# Models
from customers.models import Customer


class Loan(models.Model):
    """Loans model"""
    class Status(models.IntegerChoices):
        """Loan status"""
        PENDING = 1
        ACTIVE = 2
        REJECTED = 3
        PAID = 4

    amount = models.DecimalField(max_digits=12, decimal_places=2)
    outstanding = models.DecimalField(
        max_digits=12, decimal_places=2,
    )
    status = models.PositiveSmallIntegerField(
        choices=Status.choices,
        default=Status.PENDING
    )
    contract_version = models.CharField(max_length=30, null=True, blank=True)
    maximum_payment_date = models.DateTimeField()
    taken_at = models.DateTimeField(null=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    external_id = models.CharField(max_length=60, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Loan for {self.customer} of {self.amount} with status {self.status}'


@receiver(pre_save, sender=Loan)
def loan_pre_created_handler(instance: Loan, **kwargs):
    """
    Pre-save signal for Loan model 
    """
    if instance.status == Loan.Status.REJECTED:
        previous = Loan.objects.get(id=instance.id)
        if previous != Loan.Status.PENDING:
            raise ValidationError('Only pending loans can be rejected')

    if instance.outstanding == 0 and instance.status != Loan.Status.PAID:
        instance.status = Loan.Status.PAID


@receiver(post_save, sender=Loan)
def loan_created_handler(instance: Loan, **kwargs):
    """
    Post-save signal for Loan model
    """
    if instance.status == Loan.Status.ACTIVE and not instance.taken_at:
        instance.taken_at = timezone.now()
        instance.customer.save()
