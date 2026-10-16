from django.db import connection
from django.http import JsonResponse
from django.shortcuts import render
from apps.catalog.models import Product

def home(request):
    products = Product.objects.filter(status=Product.Status.ACTIVE).select_related("category", "seller")[:12]
    return render(request, "storefront/home.html", {"products": products})

def live_health(request):
    return JsonResponse({"status": "live"})

def ready_health(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()
        return JsonResponse({"status": "ready"})
    except Exception:
        return JsonResponse({"status": "not_ready"}, status=503)
