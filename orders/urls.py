from django.urls import path
from .views import (
    CheckoutView,
    OrderHistoryView,
    OrderStatusUpdateView,
    PaymentStatusUpdateView,
    AdminDashboardView,
    AdminOrderListView
)

urlpatterns = [
    path('checkout/', CheckoutView.as_view()),
    path('history/', OrderHistoryView.as_view()),
    path('<int:order_id>/status/', OrderStatusUpdateView.as_view()),
    path('<int:order_id>/payment-status/', PaymentStatusUpdateView.as_view()),
    path('admin-dashboard/', AdminDashboardView.as_view()),
    path('admin-orders/', AdminOrderListView.as_view()),
]