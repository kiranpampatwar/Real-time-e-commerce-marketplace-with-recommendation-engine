from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from apps.catalog.models import Product
from .models import Cart, CartItem
from .serializers import CartItemSerializer

def get_or_create_cart(user):
    return Cart.objects.get_or_create(buyer=user)[0]

class CartView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        cart = get_or_create_cart(request.user)
        items = cart.items.select_related("product").all()
        return Response(CartItemSerializer(items, many=True).data)

class CartItemCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        cart = get_or_create_cart(request.user)
        product = get_object_or_404(Product, pk=request.data.get("product"))
        quantity = int(request.data.get("quantity", 1))
        if quantity <= 0:
            return Response({"detail": "Quantity must be positive."}, status=400)
        available = getattr(product, "inventory", None)
        if not available or available.available_quantity < quantity:
            return Response({"detail": "Insufficient stock."}, status=409)
        item, created = CartItem.objects.get_or_create(cart=cart, product=product, defaults={"quantity": quantity})
        if not created:
            new_quantity = item.quantity + quantity
            if available.available_quantity < new_quantity:
                return Response({"detail": "Insufficient stock."}, status=409)
            item.quantity = new_quantity
            item.save(update_fields=["quantity"])
        return Response(CartItemSerializer(item).data, status=status.HTTP_201_CREATED)

class CartItemDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, pk):
        cart = get_or_create_cart(request.user)
        item = get_object_or_404(CartItem, pk=pk, cart=cart)
        quantity = int(request.data.get("quantity", item.quantity))
        if quantity <= 0:
            item.delete()
            return Response(status=204)
        if item.product.inventory.available_quantity < quantity:
            return Response({"detail": "Insufficient stock."}, status=409)
        item.quantity = quantity
        item.save(update_fields=["quantity"])
        return Response(CartItemSerializer(item).data)

    def delete(self, request, pk):
        cart = get_or_create_cart(request.user)
        item = get_object_or_404(CartItem, pk=pk, cart=cart)
        item.delete()
        return Response(status=204)
