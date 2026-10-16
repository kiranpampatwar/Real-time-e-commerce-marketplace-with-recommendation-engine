from django.db import models
from apps.catalog.models import Product

class InventoryItem(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name="inventory")
    available_quantity = models.PositiveIntegerField(default=0)
    reserved_quantity = models.PositiveIntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product.name}: {self.available_quantity} available"

class StockMovement(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name="stock_movements")
    quantity_delta = models.IntegerField()
    reason = models.CharField(max_length=100)
    reference = models.CharField(max_length=120, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
