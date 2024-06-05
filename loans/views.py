"""Loans views"""

# Django REST Framework
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework import status

# Models
from loans.models import Loan

# Serializers
from loans.serializers import LoanSerializer


class LoanListView(ListCreateAPIView):
    """Loan list view"""
    queryset = Loan.objects.filter(status=Loan.Status.ACTIVE)
    serializer_class = LoanSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data={
            **request.data, "status": Loan.Status.ACTIVE
        })
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)