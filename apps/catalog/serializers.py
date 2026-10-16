from rest_framework import serializers
from .models import Category, Product

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "slug"]

class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="category.name", read_only=True)
    seller_name = serializers.CharField(source="seller.username", read_only=True)
    available_quantity = serializers.IntegerField(source="inventory.available_quantity", read_only=True, default=0)

    class Meta:
        model = Product
        fields = [
            "id", "name", "slug", "description", "price", "status",
            "category", "category_name", "seller_name", "available_quantity",
        ]
        read_only_fields = ["seller_name", "available_quantity"]
