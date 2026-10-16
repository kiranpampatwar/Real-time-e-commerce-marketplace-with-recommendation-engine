from rest_framework import serializers
from .models import InventoryItem

class InventorySerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.name", read_only=True)
    class Meta:
        model = InventoryItem
        fields = ["id", "product", "product_name", "available_quantity", "reserved_quantity", "updated_at"]
