from decimal import Decimal
from django.contrib.auth import get_user_model
from django.test import TestCase
from apps.catalog.models import Category, Product
from apps.inventory.models import InventoryItem
from apps.cart.models import Cart, CartItem
from apps.orders.services import create_order_from_cart

class CheckoutServiceTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.buyer = User.objects.create_user(username="buyer", password="Pass12345!")
        self.seller = User.objects.create_user(username="seller", password="Pass12345!", role="seller")
        category = Category.objects.create(name="Test", slug="test")
        self.product = Product.objects.create(
            seller=self.seller,
            category=category,
            name="Item",
            slug="item",
            description="",
            price=Decimal("100.00"),
            status=Product.Status.ACTIVE,
        )
        InventoryItem.objects.create(product=self.product, available_quantity=2)
        cart = Cart.objects.create(buyer=self.buyer)
        CartItem.objects.create(cart=cart, product=self.product, quantity=1)

    def test_checkout_reserves_stock(self):
        order = create_order_from_cart(buyer=self.buyer, idempotency_key="checkout-12345")
        self.product.inventory.refresh_from_db()
        self.assertEqual(order.total_amount, Decimal("100.00"))
        self.assertEqual(self.product.inventory.available_quantity, 1)
        self.assertEqual(self.product.inventory.reserved_quantity, 1)
