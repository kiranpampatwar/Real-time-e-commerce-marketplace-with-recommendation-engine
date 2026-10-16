from decimal import Decimal
from django.db import transaction
from django.core.exceptions import ValidationError
from apps.cart.models import Cart
from apps.inventory.services import reserve_stock, consume_reserved_stock, InsufficientStock
from .models import Order, OrderItem

@transaction.atomic
def create_order_from_cart(*, buyer, idempotency_key: str) -> Order:
    existing = Order.objects.filter(idempotency_key=idempotency_key).first()
    if existing:
        return existing

    cart = Cart.objects.select_for_update().filter(buyer=buyer).first()
    if not cart:
        raise ValidationError("Cart does not exist.")

    items = list(cart.items.select_related("product", "product__inventory"))
    if not items:
        raise ValidationError("Cart is empty.")

    total = Decimal("0.00")
    for item in items:
        total += item.product.price * item.quantity

    order = Order.objects.create(
        buyer=buyer,
        status=Order.Status.PENDING_PAYMENT,
        total_amount=total,
        idempotency_key=idempotency_key,
    )

    for item in items:
        reserve_stock(
            product_id=item.product_id,
            quantity=item.quantity,
            reference=f"order:{order.id}",
        )
        OrderItem.objects.create(
            order=order,
            product_id_snapshot=item.product_id,
            product_name=item.product.name,
            unit_price=item.product.price,
            quantity=item.quantity,
        )

    cart.items.all().delete()
    return order

@transaction.atomic
def confirm_demo_payment(*, order: Order) -> Order:
    locked = Order.objects.select_for_update().get(pk=order.pk)
    if locked.status == Order.Status.CONFIRMED:
        return locked
    if locked.status != Order.Status.PENDING_PAYMENT:
        raise ValidationError("Order is not awaiting payment.")

    for item in locked.items.all():
        consume_reserved_stock(
            product_id=item.product_id_snapshot,
            quantity=item.quantity,
            reference=f"order:{locked.id}",
        )

    locked.status = Order.Status.CONFIRMED
    locked.payment_reference = f"DEMO-{locked.id:06d}"
    locked.save(update_fields=["status", "payment_reference"])
    return locked
