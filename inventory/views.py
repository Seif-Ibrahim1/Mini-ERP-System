from rest_framework import viewsets, permissions
from .models import Product, StockMovementLog
from .serializers import ProductSerializer, StockLogSerializer
from .permissions import IsAdminOrReadOnly

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrReadOnly]

class StockLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = StockMovementLog.objects.select_related('product', 'user').all()
    serializer_class = StockLogSerializer
    permission_classes = [permissions.IsAuthenticated]