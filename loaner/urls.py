"""URL configuration for loaner project"""

# Django
from django.contrib import admin
from django.urls import path

# Third-party
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

# Views
from loans.views import LoanListView
from customers.views import CustomerListView, CustomerBulkCreationView, CustomerBalanceView
from payments.views import PaymentListView

urlpatterns = [
    path("", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger"),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),

    path("api/v1/customers/", CustomerListView.as_view(), name="customers-list"),
    path("api/v1/customers/bulk", CustomerBulkCreationView.as_view(), name="customers-bulk"),
    path("api/v1/customers/<str:external_id>/balance", CustomerBalanceView.as_view(), name="customer-balance"),

    path("api/v1/payments/", PaymentListView.as_view(), name="payments-list"),

    path("api/v1/loans/", LoanListView.as_view(), name="loans-list"),

    path("admin/", admin.site.urls),
]
