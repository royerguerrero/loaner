"""Payment admin"""

# Django
from django.contrib import admin

# Models
from payments.models import Payment, PaymentDetail

class PaymentDetailInline(admin.StackedInline):
    """Payment detail inline admin"""
    model = PaymentDetail
    extra = 1
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    """Payment admin"""
    list_display = ('customer', 'total_amount', 'status', 'external_id', 'created_at', 'updated_at')
    list_filter = ('status',)
    search_fields = ('customer__user__email', 'customer__user__username', 'external_id')
    readonly_fields = ('created_at', 'updated_at')
    inlines = (PaymentDetailInline,)
