from django.urls import path
from .views import InventoryDetailView
urlpatterns = [path("<int:product_id>/", InventoryDetailView.as_view())]
