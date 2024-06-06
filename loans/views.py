"""Loans views"""

# Django REST Framework
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

# Models
from loans.models import Loan
from customers.models import Customer

# Serializers
from loans.serializers import LoanSerializer
from customers.serializers import CustomerBalanceSerializer, CustomerSerializer

# Build-ins
from datetime import datetime, timedelta


class LoanListView(ListCreateAPIView):
    """Loan list view"""
    queryset = Loan.objects.filter(status=Loan.Status.ACTIVE)
    serializer_class = LoanSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        customer = Customer.objects.get(
            external_id=serializer.validated_data['customer']['external_id']
        )
        customer_balance_serializer = CustomerBalanceSerializer(customer)

        if customer_balance_serializer.data['available_amount'] < serializer.validated_data['amount']:
            raise ValidationError('Customer does not have enough credit')

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
