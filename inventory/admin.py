from django.contrib import admin
from .models import Product, StockMovementLog

# Register your models here.
admin.site.register(Product)
admin.site.register(StockMovementLog)