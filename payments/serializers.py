"""Payment serializers"""

# Django REST Framework
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

# Models
from payments.models import Payment, PaymentDetail


class PaymentSerializer(ModelSerializer):
    """Payment serializer"""
    status = serializers.IntegerField(read_only=True)
    loan_external_ids = serializers.SerializerMethodField()

    class Meta:
        model = Payment
        fields = (
            'external_id', 'total_amount', 'status', 'loan_external_ids'
        )

    def get_loan_external_ids(self, payment):
        """
        Retrieves the external IDs of loans associated with a payment.
        """
        payment_details = PaymentDetail.objects.filter(
            payment__external_id=payment['external_id']
        )

        return [
            {'loan_external_id': pd.loan.external_id, 'payment_amount': pd.amount} 
            for pd in payment_details
        ]
