from django.urls import path
from .views import CheckoutView, OrderListView, OrderDetailView, DemoPaymentConfirmView

urlpatterns = [
    path("checkout/", CheckoutView.as_view()),
    path("", OrderListView.as_view()),
    path("<int:pk>/", OrderDetailView.as_view()),
    path("<int:pk>/confirm-demo-payment/", DemoPaymentConfirmView.as_view()),
]
