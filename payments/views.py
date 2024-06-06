"""Payments views"""

# Django
from django.utils import timezone

# Django REST Framework
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

# Models
from payments.models import Payment, PaymentDetail
from customers.models import Customer
from loans.models import Loan

# Serializers
from payments.serializers import PaymentSerializer
from customers.serializers import CustomerBalanceSerializer


class PaymentCustomerView(ListCreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return super().get_queryset().filter(
            customer__external_id=self.kwargs['external_id']
        )

    def create(self, request, *args, **kwargs):
        customer = Customer.objects.get(external_id=self.kwargs['external_id'])
        customer_balance = CustomerBalanceSerializer(customer)

        payment_status = Payment.Status.REJECTED
        if int(request.data['total_amount']) < customer_balance.data['total_debt']:
            payment_status = Payment.Status.COMPLETED

        customer_loans = Loan.objects.filter(
            customer__external_id=customer_balance.data['external_id'],
            status=Loan.Status.ACTIVE
        ).order_by('amount')

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        payment = Payment.objects.create(
            **serializer.validated_data,
            status=payment_status,
            customer=customer,
            paid_at=timezone.now()
        )

        total_amount = serializer.validated_data['total_amount']
        for loan in customer_loans:
            if total_amount < 0:
                break
            
            amount = loan.outstanding if total_amount > loan.outstanding else total_amount
            payment_detail = PaymentDetail.objects.create(
                amount=amount,
                payment=payment,
                loan=loan,
            )
            total_amount = total_amount - loan.outstanding
            loan.outstanding = loan.outstanding - amount
            loan.save()


        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
