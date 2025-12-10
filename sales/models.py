from django.db import models
from django.conf import settings
from inventory.models import Product

class Customer(models.Model):
    code = models.CharField(max_length=20, unique=True, db_index=True)
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    address = models.TextField()
    email = models.EmailField()
    opening_balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.code} - {self.name}"

class Sequence(models.Model):
    key = models.CharField(max_length=50, unique=True) 
    last_number = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.key}: {self.last_number}"

class SalesOrder(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        CONFIRMED = 'CONFIRMED', 'Confirmed'
        CANCELLED = 'CANCELLED', 'Cancelled'

    # made it to sequence as I had time
    order_number = models.CharField(max_length=20, unique=True, editable=False)
    
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name='orders')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    order_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    
    # to avoid re-calc
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def __str__(self):
        return self.order_number

class SalesOrderItem(models.Model):
    order = models.ForeignKey(SalesOrder, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    qty = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def total(self):
        return self.qty * self.price