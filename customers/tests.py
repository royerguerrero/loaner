"""Customer tests"""

# Django
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

# Django REST Framework
from rest_framework.test import APIClient
from rest_framework import status

# Models
from customers.models import Customer
from loans.models import Loan

# Build-ins
import uuid
from django.urls import reverse


class CustomerAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.customer = Customer.objects.create(
            score=1000,
            preapproved_at='2021-01-01T00:00:00Z',
            external_id=str(uuid.uuid4())
        )

        self.list_url = reverse('customers-list')
        self.bulk_url = reverse('customers-bulk')
        self.balance_url = reverse(
            'customer-balance', 
            kwargs={'external_id': self.customer.external_id}
        )

    def test_get_customers(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_customer(self):
        data = {
            'score': 2000,
            'preapproved_at': timezone.now(),
            'external_id': str(uuid.uuid4())
        }

        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Customer.objects.count(), 2)
        self.assertEqual(
            Customer.objects.get(external_id=data['external_id']).external_id,
            data['external_id']
        )
        self.assertEqual(response.data['status'], Customer.Status.ACTIVE)

    def test_get_customer_balance(self):
        response = self.client.get(self.balance_url)
        # TODO: Complete this method
