"""Customers views"""

# Django REST Framework
from rest_framework.generics import ListCreateAPIView, CreateAPIView, RetrieveAPIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

# Model
from customers.models import Customer

# Serializers
from customers.serializers import CustomerSerializer, CustomerBalanceSerializer


class CustomerListView(ListCreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


class CustomerBulkCreationView(CreateAPIView):
    serializer_class = CustomerSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class CustomerBalanceView(RetrieveAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerBalanceSerializer
    lookup_field = 'external_id'
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
