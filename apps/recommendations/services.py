from collections import Counter
from django.db.models import Count
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from apps.catalog.models import Product
from .models import ProductInteraction

def popular_products(limit=8):
    return list(
        Product.objects.filter(status=Product.Status.ACTIVE)
        .annotate(interactions=Count("productinteraction"))
        .order_by("-interactions", "-created_at")[:limit]
    )

def personalized_products(user, limit=8):
    recent = list(
        ProductInteraction.objects.filter(user=user)
        .select_related("product", "product__category")
        .order_by("-created_at")[:20]
    )
    if not recent:
        return popular_products(limit)

    products = list(
        Product.objects.filter(status=Product.Status.ACTIVE)
        .select_related("category")
    )
    if len(products) < 2:
        return products[:limit]

    corpus = [
        f"{p.name} {p.description} {p.category.name}"
        for p in products
    ]
    matrix = TfidfVectorizer(stop_words="english").fit_transform(corpus)

    recent_ids = [x.product_id for x in recent]
    index_map = {p.id: idx for idx, p in enumerate(products)}
    seed_indexes = [index_map[pid] for pid in recent_ids if pid in index_map]
    if not seed_indexes:
        return popular_products(limit)

    profile = matrix[seed_indexes].mean(axis=0)
    scores = cosine_similarity(profile, matrix).ravel()
    ranked = sorted(range(len(products)), key=lambda i: scores[i], reverse=True)

    seen = set(recent_ids)
    results = [products[i] for i in ranked if products[i].id not in seen]
    return results[:limit]
