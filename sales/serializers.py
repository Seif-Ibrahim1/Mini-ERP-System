from rest_framework import serializers
from .models import SalesOrder, SalesOrderItem, Customer
from inventory.models import Product
from .services import create_order

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'code', 'name', 'phone', 'address', 'email', 'opening_balance']

class SalesOrderItemReadSerializer(serializers.ModelSerializer):
    product_sku = serializers.CharField(source='product.sku')
    product_name = serializers.CharField(source='product.name')

    class Meta:
        model = SalesOrderItem
        fields = ['id', 'product_id', 'product_sku', 'product_name', 'qty', 'price', 'total']

class SalesOrderReadSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source='customer.name')
    customer_code = serializers.CharField(source='customer.code')
    created_by_name = serializers.CharField(source='created_by.username')
    items = SalesOrderItemReadSerializer(many=True, read_only=True)

    class Meta:
        model = SalesOrder
        fields = [
            'id', 'order_number', 'order_date', 'status', 'total_amount','customer',
            'customer_code', 'customer_name', 'created_by', 'created_by_name','items'
        ]

class SalesOrderItemSerializer(serializers.ModelSerializer):
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), 
        source='product'
    )
    
    class Meta:
        model = SalesOrderItem
        fields = ['product_id', 'qty', 'price', 'total']
        read_only_fields = ['price', 'total']

class SalesOrderCreateSerializer(serializers.ModelSerializer):
    items = SalesOrderItemSerializer(many=True)

    class Meta:
        model = SalesOrder
        fields = ['id', 'order_number', 'customer', 'status', 'total_amount', 'items']
        read_only_fields = ['id', 'order_number', 'status', 'total_amount']

    def validate_items(self, value):
        if not value:
            raise serializers.ValidationError("order must contain at least one item.")
        return value

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        user = self.context['request'].user
        customer = validated_data['customer']
        
        return create_order(user=user, customer=customer, items_data=items_data)
    
class DashboardSerializer(serializers.Serializer):
    total_customers = serializers.IntegerField()
    today_sales_revenue = serializers.DecimalField(max_digits=12, decimal_places=2)
    low_stock_alert = serializers.IntegerField()
    generated_at = serializers.DateTimeField()