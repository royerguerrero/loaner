"""Payment serializers"""

# Django REST Framework
from rest_framework.serializers import ModelSerializer

# Models
from payments.models import Payment

class PaymentSerializer(ModelSerializer):
    class Meta:
        model = Payment
        fields = ['external_id', 'total_amount', 'status']
