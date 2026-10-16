from rest_framework import generics, permissions
from .models import InventoryItem
from .serializers import InventorySerializer

class InventoryDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = InventorySerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "product_id"

    def get_queryset(self):
        qs = InventoryItem.objects.select_related("product", "product__seller")
        if self.request.user.is_staff:
            return qs
        return qs.filter(product__seller=self.request.user)
