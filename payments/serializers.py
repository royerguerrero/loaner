"""Payment serializers"""

# Django REST Framework
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

# Models
from payments.models import Payment

class PaymentSerializer(ModelSerializer):
    """Payment serializer"""
    customer_external_id = serializers.CharField(source='customer.external_id')
    loan_external_id = serializers.CharField(source='loan.external_id')
    payment_date = serializers.DateField(source='paid_at')

    class Meta:
        model = Payment
        fields = (
            'external_id', 'customer_external_id', 'loan_external_id',
            # 'payment_date', 'status', 'total_amount', 'payment_amount'
            'payment_date', 'status', 'total_amount'
        )
