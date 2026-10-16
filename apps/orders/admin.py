from django.contrib import admin
from .models import Order, OrderItem, PaymentWebhookEvent
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(PaymentWebhookEvent)
