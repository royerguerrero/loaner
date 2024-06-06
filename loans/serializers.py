"""Loans serializers"""

# Django
from django.utils import timezone

# Django REST Framework
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

# Models
from loans.models import Loan
from customers.models import Customer

# Build-ins
from datetime import timedelta


class LoanSerializer(ModelSerializer):
    """Loan serializer"""
    customer_external_id = serializers.CharField(
        source='customer.external_id',
    )

    class Meta:
        model = Loan
        fields = (
            'external_id', 'customer_external_id', 'amount',
            'outstanding', 'status', 'maximum_payment_date',
        )
        read_only_fields = ('outstanding', 'maximum_payment_date', 'status')

    def create(self, validated_data):
        external_id = validated_data.pop('customer')['external_id']
        customer = get_object_or_404(Customer, external_id=external_id)
        return Loan.objects.create(
            customer=customer,
            **{
                **validated_data,
                "status": Loan.Status.ACTIVE,
                "outstanding": validated_data['amount'],
                "maximum_payment_date": timezone.now() + timedelta(weeks=30)
            },
        )
