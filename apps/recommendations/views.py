from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.catalog.serializers import ProductSerializer
from .services import personalized_products, popular_products

class RecommendationView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        limit = min(int(request.query_params.get("limit", 8)), 20)
        if request.user.is_authenticated:
            products = personalized_products(request.user, limit)
            strategy = "content_based"
        else:
            products = popular_products(limit)
            strategy = "popular"
        return Response({
            "strategy": strategy,
            "items": ProductSerializer(products, many=True).data,
        })
