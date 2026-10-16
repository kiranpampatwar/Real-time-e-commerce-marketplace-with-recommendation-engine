from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from apps.catalog.models import Category, Product
from apps.inventory.models import InventoryItem

class Command(BaseCommand):
    help = "Seed deterministic demo products for local development."

    def handle(self, *args, **options):
        User = get_user_model()
        seller, _ = User.objects.get_or_create(
            username="demo_seller",
            defaults={"email": "seller@example.com", "role": User.Role.SELLER},
        )
        if not seller.has_usable_password():
            seller.set_password("Seller123!")
            seller.save(update_fields=["password"])

        data = {
            "Electronics": [
                ("Wireless Headphones", "Noise-cancelling over-ear headphones", "4999.00", 25),
                ("Mechanical Keyboard", "RGB mechanical keyboard", "3499.00", 30),
                ("Smart Watch", "Fitness tracking smartwatch", "6999.00", 18),
            ],
            "Sports": [
                ("Running Shoes", "Lightweight daily running shoes", "2999.00", 40),
                ("Yoga Mat", "Non-slip exercise yoga mat", "999.00", 50),
            ],
            "Home": [
                ("Coffee Maker", "Compact drip coffee maker", "2599.00", 16),
                ("Desk Lamp", "LED desk lamp with brightness control", "1499.00", 28),
            ],
        }

        created = 0
        for category_name, products in data.items():
            category, _ = Category.objects.get_or_create(
                name=category_name,
                defaults={"slug": slugify(category_name)},
            )
            for name, description, price, stock in products:
                product, was_created = Product.objects.get_or_create(
                    slug=slugify(name),
                    defaults={
                        "seller": seller,
                        "category": category,
                        "name": name,
                        "description": description,
                        "price": price,
                        "status": Product.Status.ACTIVE,
                    },
                )
                InventoryItem.objects.get_or_create(
                    product=product,
                    defaults={"available_quantity": stock},
                )
                created += int(was_created)

        self.stdout.write(self.style.SUCCESS(f"Demo data ready. New products created: {created}"))
