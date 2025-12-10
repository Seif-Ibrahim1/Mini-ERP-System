from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import SalesOrder, Customer
from .serializers import SalesOrderCreateSerializer, SalesOrderReadSerializer, CustomerSerializer, DashboardSerializer
from .services import confirm_order, cancel_order, generate_sales_excel
from .permissions import IsSalesOrAdmin, CustomerPermission, IsAdmin

from drf_spectacular.utils import extend_schema
from .selectors import get_dashboard_stats

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

    @extend_schema(request=None) 
    @action(detail=True, methods=['post'])
    def confirm(self, request, pk=None):
        order = self.get_object()
        try:
            confirm_order(order=order, user=request.user)
            return Response({'status': 'Order Confirmed', 'stock_deducted': True})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    @extend_schema(request=None) 
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        order = self.get_object()
        try:
            cancel_order(order, request.user)
            return Response({'status': 'Order Cancelled'})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    @extend_schema(request=None)
    @action(detail=False, methods=['get'], url_path='export-excel')
    def export_excel(self, request):
        if not request.user.role == 'ADMIN':
             return Response({'error': 'Admins only'}, status=403)
             
        return generate_sales_excel()
        

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [CustomerPermission]
    search_fields = ['name', 'email', 'phone']

class DashboardViewSet(viewsets.ViewSet):
    permission_classes = [IsAdmin]

    @extend_schema(responses={200: DashboardSerializer})
    def list(self, request):
        stats_dto = get_dashboard_stats()
        serializer = DashboardSerializer(stats_dto)
        return Response(serializer.data)

