from django.core.exceptions import ValidationError
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import Order
from .serializers import OrderSerializer
from .services import create_order_from_cart, confirm_demo_payment

class CheckoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        key = request.data.get("idempotency_key")
        if not key or len(key) < 8:
            return Response({"detail": "A valid idempotency_key is required."}, status=400)
        try:
            order = create_order_from_cart(buyer=request.user, idempotency_key=key)
        except ValidationError as exc:
            return Response({"detail": exc.message}, status=400)
        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)

class OrderListView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        qs = Order.objects.filter(buyer=request.user).prefetch_related("items").order_by("-created_at")
        return Response(OrderSerializer(qs, many=True).data)

class OrderDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, pk):
        order = get_object_or_404(Order.objects.prefetch_related("items"), pk=pk, buyer=request.user)
        return Response(OrderSerializer(order).data)

class DemoPaymentConfirmView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, pk):
        order = get_object_or_404(Order, pk=pk, buyer=request.user)
        try:
            order = confirm_demo_payment(order=order)
        except ValidationError as exc:
            return Response({"detail": exc.message}, status=409)
        return Response(OrderSerializer(order).data)
