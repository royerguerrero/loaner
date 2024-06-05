"""Customers views"""

# Django REST Framework
from rest_framework.generics import ListCreateAPIView, CreateAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework import status

# Model
from customers.models import Customer

# Serializers
from customers.serializers import CustomerSerializer, CustomerBalanceSerializer


class CustomerListView(ListCreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    def create(self, request, *args, **kwargs):
        """Handle customer creation"""
        serializer = self.get_serializer(data={
            **request.data, "status": Customer.Status.ACTIVE
        })
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class CustomerBulkCreationView(CreateAPIView):
    serializer_class = CustomerSerializer

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class CustomerBalanceView(RetrieveAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerBalanceSerializer
    lookup_field = 'external_id'
