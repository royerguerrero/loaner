"""Customer Serializer"""

# Django REST Framework
from rest_framework.serializers import ModelSerializer

# Models
from customers.models import Customer


class CustomerSerializer(ModelSerializer):
    """Customer serializer"""
    class Meta:
        model = Customer
        fields = ('external_id', 'status', 'score', 'preaprroved_at')
        read_only_fields = ('status',)
