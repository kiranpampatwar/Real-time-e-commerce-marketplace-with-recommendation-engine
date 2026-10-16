from django.db.models import Q
from rest_framework import generics, permissions
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer
from .permissions import IsSellerOwnerOrReadOnly

class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class ProductListCreateView(generics.ListCreateAPIView):
    serializer_class = ProductSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    def get_queryset(self):
        qs = Product.objects.select_related("category", "seller").filter(status=Product.Status.ACTIVE)
        q = self.request.query_params.get("q")
        category = self.request.query_params.get("category")
        ordering = self.request.query_params.get("ordering", "-created_at")
        if q:
            qs = qs.filter(Q(name__icontains=q) | Q(description__icontains=q))
        if category:
            qs = qs.filter(category__slug=category)
        allowed_ordering = {"price", "-price", "name", "-name", "created_at", "-created_at"}
        if ordering in allowed_ordering:
            qs = qs.order_by(ordering)
        return qs

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)

class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.select_related("category", "seller").all()
    serializer_class = ProductSerializer
    lookup_field = "slug"
    permission_classes = [IsSellerOwnerOrReadOnly]
