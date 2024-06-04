"""Payments views"""

# Django REST Framework
from rest_framework.generics import ListCreateAPIView

# Models
from payments.models import Payment

# Serializers
from payments.serializers import PaymentSerializer

class PaymentListView(ListCreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
