from .views import *

from django.urls import path

urlpatterns = [
    path("", InvoiceCreateAPIView.as_view(), name="invoice_self_creation"),
    path("<int:id>/", InvoiceRetrieveUpdateDestroyAPIView.as_view(), name="plan_self_creation_points"),
]
