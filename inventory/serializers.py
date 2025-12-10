from rest_framework import serializers
from .models import Product, StockMovementLog

class ProductSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False)
    class Meta:
        model = Product
        fields = ['id', 'sku', 'name', 'category', 'cost_price', 'selling_price', 'stock_qty', 'image']

class StockLogSerializer(serializers.ModelSerializer):
    product_sku = serializers.CharField(source='product.sku', read_only=True)
    user_name = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = StockMovementLog
        fields = ['id', 'product', 'product_sku', 'qty', 'user', 'user_name', 'timestamp', 'note']