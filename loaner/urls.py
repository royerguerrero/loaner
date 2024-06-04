"""URL configuration for loaner project"""

# Django
from django.contrib import admin
from django.urls import path, include

# Third-party
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

# Views
from loans.views import LoanListView
from customers.views import CustomerListView
from payments.views import PaymentListView

urlpatterns = [
    path("", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger"),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),

    path("api/v1/customers/", CustomerListView.as_view(), name="customers-list"),
    path("api/v1/payments/", PaymentListView.as_view(), name="payments-list"),
    path("api/v1/loans/", LoanListView.as_view(), name="loan-list"),


    path("admin/", admin.site.urls),
]
