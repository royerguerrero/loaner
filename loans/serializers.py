"""Loans serializers"""

# Django REST Framework
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

# Models
from loans.models import Loan


class LoanSerializer(ModelSerializer):
    """Loan serializer"""
    customer_external_id = serializers.CharField(source='customer.external_id')

    class Meta:
        model = Loan
        fields = ['external_id', 'customer_external_id', 'amount', 'outstanding', 'status']
