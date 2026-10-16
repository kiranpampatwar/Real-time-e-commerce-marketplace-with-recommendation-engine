from django.db import transaction
from django.core.exceptions import ValidationError
from .models import InventoryItem, StockMovement

class InsufficientStock(Exception):
    pass

@transaction.atomic
def reserve_stock(product_id: int, quantity: int, reference: str) -> InventoryItem:
    if quantity <= 0:
        raise ValidationError("Quantity must be positive.")
    inventory = InventoryItem.objects.select_for_update().get(product_id=product_id)
    if inventory.available_quantity < quantity:
        raise InsufficientStock("Insufficient stock.")
    inventory.available_quantity -= quantity
    inventory.reserved_quantity += quantity
    inventory.save(update_fields=["available_quantity", "reserved_quantity", "updated_at"])
    StockMovement.objects.create(
        product_id=product_id,
        quantity_delta=-quantity,
        reason="reservation",
        reference=reference,
    )
    return inventory

@transaction.atomic
def consume_reserved_stock(product_id: int, quantity: int, reference: str) -> InventoryItem:
    inventory = InventoryItem.objects.select_for_update().get(product_id=product_id)
    if inventory.reserved_quantity < quantity:
        raise ValidationError("Reserved quantity is insufficient.")
    inventory.reserved_quantity -= quantity
    inventory.save(update_fields=["reserved_quantity", "updated_at"])
    StockMovement.objects.create(
        product_id=product_id,
        quantity_delta=0,
        reason="reservation_consumed",
        reference=reference,
    )
    return inventory
