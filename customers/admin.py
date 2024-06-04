"""Customers admin"""

# Django
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Models
from django.contrib.auth.models import User
from customers.models import Customer


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    """Customer admin"""
    list_display = ('user', 'score', 'status', 'preaprroved_at', 'external_id', 'created_at', 'updated_at')
    list_filter = ('status',)
    search_fields = ('user__email', 'user__username', 'external_id')
    readonly_fields = ('created_at', 'updated_at')


class CustomerInline(admin.StackedInline):
    """Customer inline"""
    model = Customer
    can_delete = False
    verbose_name_plural = 'customers'


class UserAdmin(BaseUserAdmin):
    """User Admin"""
    inlines = (CustomerInline,)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
