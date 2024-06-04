"""Payments Models"""

# Django
from django.db import models

# Models
from customers.models import Customer
from loans.models import Loan

class Payment(models.Model):
    """Payments model"""
    class Status(models.IntegerChoices):
        """Payment status"""
        COMPLETED = 1
        REJECTED = 2


    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.PositiveSmallIntegerField(choices=Status.choices)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    external_id = models.CharField(max_length=60, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class PaymentDetail(models.Model):
    """Payments details model"""
    amount = models.DecimalField(max_digits=20, decimal_places=10)
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE)
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
