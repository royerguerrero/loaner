"""Customer Serializer"""

# Django REST Framework
from rest_framework.serializers import ModelSerializer, Serializer
from rest_framework import serializers

# Django
from django.db.models import Sum

# Models
from customers.models import Customer
from loans.models import Loan


class CustomerSerializer(ModelSerializer):
    """Customer serializer"""
    class Meta:
        model = Customer
        fields = ('external_id', 'status', 'score', 'preapproved_at')
        read_only_fields = ('status',)


class CustomerBalanceSerializer(ModelSerializer):
    """Customer balance serializer"""
    total_debt = serializers.SerializerMethodField()
    available_amount = serializers.SerializerMethodField()

    class Meta:
        model = Customer
        fields = ('external_id', 'score', 'available_amount', 'total_debt',)
        read_only_fields = (
            'external_id',
            'score',
            'available_amount',
            'total_debt',
        )

    def get_total_debt(self, customer):
        """
        Return total debt. the total debt is the sum of all outstanding loans
        """
        return Loan.objects.filter(
            external_id=customer.external_id
        ).aggregate(
            total_debt=Sum('outstanding')
        ).get('total_debt') or 0

    def get_available_amount(self, customer):
        """
        Return available amount. the available amount is the score minus the total debt
        """
        return customer.score - self.get_total_debt(customer)
