"""Loans views"""

# Django REST Framework
from rest_framework import generics

# Models
from loans.models import Loan

# Serializers
from loans.serializers import LoanSerializer


class LoanListView(generics.ListCreateAPIView):
    """Loan list view"""
    queryset = Loan.objects.filter(status=Loan.Status.ACTIVE)
    serializer_class = LoanSerializer
