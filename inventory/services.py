from django.db import transaction
from django.core.exceptions import ValidationError
from .models import Product, StockMovementLog

@transaction.atomic
def adjust_stock(product: Product, qty: int, user, note: str = ""):
    # for race conditions
    product = Product.objects.select_for_update().get(id=product.id)
    
    new_qty = product.stock_qty + qty
    if new_qty < 0:
        raise ValidationError(f"Insufficient stock for {product.sku}. Available: {product.stock_qty}")

    product.stock_qty = new_qty
    product.save()

    StockMovementLog.objects.create(product=product, qty=qty, user=user, note=note)
    
    return product