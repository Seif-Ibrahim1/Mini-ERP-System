from django.db import transaction
from django.utils import timezone
from django.core.exceptions import ValidationError
from .models import SalesOrder, SalesOrderItem, Sequence
from inventory.services import adjust_stock

def get_next_order_number():
    #SO-00001
    with transaction.atomic():
        sequence, _ = Sequence.objects.select_for_update().get_or_create(key='sales_order')
        
        sequence.last_number += 1
        sequence.save()
        
        return f"SO-{sequence.last_number:05d}"
    
def create_order(user, customer, items_data: list):
    """
    this is the excpected items_data [{'product': product_obj, 'qty': 2}, ...]
    """

    with transaction.atomic():
        order_number = get_next_order_number()
        
        order = SalesOrder.objects.create(order_number=order_number, customer=customer, created_by=user,
                                           status=SalesOrder.Status.PENDING)

        total_amount = 0
        for item in items_data:
            product = item['product']
            qty = item['qty']
            
            price = product.selling_price 
            
            SalesOrderItem.objects.create(order=order, product=product, qty=qty, price=price)
            total_amount += (price * qty)

        order.total_amount = total_amount
        order.save()
        
        return order

@transaction.atomic
def confirm_order(order: SalesOrder, user):
    if order.status != SalesOrder.Status.PENDING:
        raise ValidationError("only pending orders can be confirmed.")

    for item in order.items.all():
        # neg qty because we are selling
        adjust_stock(product=item.product, qty=-item.qty, user=user, note=f"Sales Order {order.order_number}")
        
    order.status = SalesOrder.Status.CONFIRMED
    order.save()
    
    return order

@transaction.atomic
def cancel_order(order: SalesOrder, user):
    if order.status == SalesOrder.Status.CANCELLED:
        raise ValidationError("order is already cancelled.")

    if order.status == SalesOrder.Status.CONFIRMED:
        for item in order.items.all():
            adjust_stock( product=item.product, qty=item.qty, user=user, note=f"Cancelled Order {order.order_number}")

    order.status = SalesOrder.Status.CANCELLED
    order.save()
    return order