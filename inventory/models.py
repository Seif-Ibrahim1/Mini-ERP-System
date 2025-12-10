from django.db import models
from django.conf import settings
from django.db.models import CheckConstraint, Q

class Product(models.Model):
    sku = models.CharField(max_length=50, unique=True, db_index=True)
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=100) # Could be FK for me personally, but Task says CharField
    
    cost_price = models.DecimalField(max_digits=10, decimal_places=2)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    stock_qty = models.IntegerField(default=0)

    class Meta:
        constraints = [
            CheckConstraint(condition=Q(stock_qty__gte=0), name='stock_non_negative')
        ]

    def __str__(self):
        return f"{self.sku} - {self.name}"

class StockMovementLog(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='stock_logs')
    qty = models.IntegerField(help_text="Negative for reduction, Positive for addition")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    note = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.product.sku} | {self.qty} | {self.timestamp}"