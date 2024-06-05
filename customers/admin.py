"""Customers admin"""

# Django
from django.contrib import admin

# Models
from customers.models import Customer


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    """Customer admin"""
    list_display = ('score', 'status', 'preapproved_at', 'external_id', 'created_at', 'updated_at')
    list_filter = ('status',)
    search_fields = ('external_id',)
    readonly_fields = ('created_at', 'updated_at')
