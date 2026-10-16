from django.urls import path
from .views import CategoryListView, ProductListCreateView, ProductDetailView

urlpatterns = [
    path("categories/", CategoryListView.as_view()),
    path("products/", ProductListCreateView.as_view()),
    path("products/<slug:slug>/", ProductDetailView.as_view()),
]
