from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import SalesOrder, Customer
from .serializers import SalesOrderCreateSerializer, SalesOrderReadSerializer, CustomerSerializer
from .services import confirm_order
from .permissions import IsSalesOrAdmin, CustomerPermission

class SalesOrderViewSet(viewsets.ModelViewSet):
    permission_classes = [IsSalesOrAdmin]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['order_number', 'customer__name']
    ordering_fields = ['order_date', 'total_amount']

    def get_queryset(self):
        return SalesOrder.objects.select_related('customer', 'created_by').prefetch_related('items__product').all()

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return SalesOrderCreateSerializer
        return SalesOrderReadSerializer

    @action(detail=True, methods=['post'])
    def confirm(self, request, pk=None):
        order = self.get_object()
        try:
            confirm_order(order=order, user=request.user)
            return Response({'status': 'Order Confirmed', 'stock_deducted': True})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        order = self.get_object()
        cancel_order(order, request.user)
        return Response({'status': 'Order Cancelled'})
        

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [CustomerPermission]
    search_fields = ['name', 'email', 'phone']