"""Loans admin"""

# Django
from django.contrib import admin

# Models
from loans.models import Loan

@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    """Loan admin"""
    list_display = ('customer', 'amount', 'status', 'contract_version', 'maximum_payment_date', 'taken_at', 'external_id', 'created_at', 'updated_at')
    list_filter = ('status',)
    search_fields = ('customer__user__email', 'customer__user__username', 'external_id')
    readonly_fields = ('created_at', 'updated_at')
