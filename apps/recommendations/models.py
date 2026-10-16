from django.conf import settings
from django.db import models
from apps.catalog.models import Product

class ProductInteraction(models.Model):
    class Event(models.TextChoices):
        VIEW = "product_view", "Product view"
        ADD_TO_CART = "add_to_cart", "Add to cart"
        PURCHASE = "purchase", "Purchase"

    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    event_type = models.CharField(max_length=30, choices=Event.choices)
    created_at = models.DateTimeField(auto_now_add=True)
