from rest_framework import serializers
from .models import SalesOrder, SalesOrderItem
from inventory.models import Product
from .services import create_order

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