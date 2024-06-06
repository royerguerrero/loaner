"""Payment tests"""

# Django
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

# Django REST Framework
from rest_framework.test import APIClient

# Models
from customers.models import Customer
from loans.models import Loan
from payments.models import Payment, PaymentDetail

# Build-ins
from datetime import timedelta
import uuid


class PaymentAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.customer = Customer.objects.create(
            external_id='1234',
            score=3000,
            preapproved_at='2021-01-01T00:00:00Z'
        )
        self.loan = Loan.objects.create(
            external_id='testing',
            amount=1000,
            outstanding=500,
            maximum_payment_date=timezone.now() + timedelta(weeks=26),
            status=Loan.Status.ACTIVE,
            customer=self.customer
        )
        self.customer_payment = reverse(
            'customer-payments',
            kwargs={'external_id': self.customer.external_id}
        )

    def test_get_payments(self):
        response = self.client.get(self.customer_payment)
        self.assertEqual(response.status_code, 200)

    def test_create_payment_in_excess_of_total_deb(self):
        data = {
            "external_id": str(uuid.uuid4()),
            "total_amount": 10000,
        }
        response = self.client.post(self.customer_payment, data, format='json')
        self.assertAlmostEqual(response.status_code, 201)
        self.assertEqual(
            Payment.objects.get(external_id=data['external_id']).status,
            Payment.Status.REJECTED.value
        )

    def test_create_payment(self):
        data = {
            "external_id": str(uuid.uuid4()),
            "total_amount": 100,
        }

        response = self.client.post(self.customer_payment, data, format='json')
        self.assertEqual(response.status_code, 201)

    def test_create_payment_settle_all_debts(self):
        customer = Customer.objects.create(
            external_id=str(uuid.uuid4()),
            score=100,
            preapproved_at='2021-01-01T00:00:00Z'
        )
        loan1 = Loan.objects.create(
            external_id=str(uuid.uuid4()),
            amount=40,
            outstanding=40,
            maximum_payment_date=timezone.now() + timedelta(weeks=26),
            status=Loan.Status.ACTIVE,
            customer=customer
        )
        loan2 = Loan.objects.create(
            external_id=str(uuid.uuid4()),
            amount=50,
            outstanding=50,
            maximum_payment_date=timezone.now() + timedelta(weeks=26),
            status=Loan.Status.ACTIVE,
            customer=customer
        )
        loan3 = Loan.objects.create(
            external_id=str(uuid.uuid4()),
            amount=10,
            outstanding=10,
            maximum_payment_date=timezone.now() + timedelta(weeks=26),
            status=Loan.Status.ACTIVE,
            customer=customer
        )

        data = {
            "external_id": str(uuid.uuid4()),
            "total_amount": 100,
        }

        url = reverse(
            'customer-payments',
            kwargs={'external_id': customer.external_id}
        )
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(len(response.data['loan_external_ids']), 3)
        self.assertEqual(
            Loan.objects.get(id=loan1.id).status,
            Loan.Status.PAID.value
        )
        self.assertEqual(
            Loan.objects.get(id=loan2.id).status,
            Loan.Status.PAID.value
        )
        self.assertEqual(
            Loan.objects.get(id=loan2.id).status,
            Loan.Status.PAID.value
        )

    def test_create_payment_partially_settle_all_debts(self):
        customer = Customer.objects.create(
            external_id=str(uuid.uuid4()),
            score=1000,
            preapproved_at='2021-01-01T00:00:00Z'
        )
        loan1 = Loan.objects.create(
            external_id=str(uuid.uuid4()),
            amount=200,
            outstanding=200,
            maximum_payment_date=timezone.now() + timedelta(weeks=26),
            status=Loan.Status.ACTIVE,
            customer=customer,
        )
        loan2 = Loan.objects.create(
            external_id=str(uuid.uuid4()),
            amount=500,
            outstanding=50,
            maximum_payment_date=timezone.now() + timedelta(weeks=26),
            status=Loan.Status.ACTIVE,
            customer=customer
        )

        data = {
            "external_id": str(uuid.uuid4()),
            "total_amount": 100,
        }

        url = reverse(
            'customer-payments',
            kwargs={'external_id': customer.external_id}
        )
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(len(response.data['loan_external_ids']), 1)
        self.assertEqual(
            response.data['loan_external_ids'][0]['payment_amount'], 100
        )
