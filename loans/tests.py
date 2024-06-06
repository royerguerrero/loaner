"""Loans tests"""

# Django
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

# Django REST Framework
from rest_framework.test import APIClient
from rest_framework import status

# Models
from loans.models import Loan
from customers.models import Customer

# Build-ins
from datetime import timedelta
import uuid


class LoanAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.customer = Customer.objects.create(
            external_id='1234',
            score=3000,
            preapproved_at='2021-01-01T00:00:00Z'
        )
        self.customer_without_score = Customer.objects.create(
            external_id='5678',
            score=0,
            preapproved_at='2021-01-01T00:00:00Z'
        )
        self.loan = Loan.objects.create(
            external_id='1234',
            amount=1000,
            outstanding=0,
            maximum_payment_date=timezone.now() + timedelta(weeks=26),
            status=Loan.Status.ACTIVE,
            customer=self.customer
        )
        self.list_url = reverse('loans-list')

    def test_get_loans(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_loan(self):
        data = {
            'external_id': str(uuid.uuid4()),
            'customer_external_id': self.customer.external_id,
            'amount': 2000
        }

        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Loan.objects.count(), 2)
        self.assertEqual(
            Loan.objects.get(
                external_id=data['customer_external_id']
            ).external_id,
            data['customer_external_id']
        )
        self.assertEqual(response.data['status'], Loan.Status.ACTIVE)

    def test_create_loan_for_a_customer_without_score(self):
        data = {
            'external_id': str(uuid.uuid4()),
            'customer_external_id': self.customer_without_score.external_id,
            'amount': 2000
        }

        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
