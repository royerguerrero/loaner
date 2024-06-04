"""Loans models"""

# Django
from django.db import models

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
    outstanding = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.PositiveSmallIntegerField(choices=Status.choices, default=Status.PENDING.value)
    contract_version = models.CharField(max_length=30)
    maximum_payment_date = models.DateTimeField()
    taken_at = models.DateTimeField()
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    external_id = models.CharField(max_length=60, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Loan for {self.customer} of {self.amount} with status {self.status}'
