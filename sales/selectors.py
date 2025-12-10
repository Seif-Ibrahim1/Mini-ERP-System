from django.db.models import Sum
from django.utils import timezone
from inventory.models import Product
from .models import Customer, SalesOrder
from .types import DashboardStats

def get_dashboard_stats() -> DashboardStats:
    today = timezone.now().date()
    total_customers = Customer.objects.count()

    revenue_data = SalesOrder.objects.filter(
        order_date=today, 
        status=SalesOrder.Status.CONFIRMED
    ).aggregate(total=Sum('total_amount'))

    today_revenue = revenue_data['total'] or 0
    low_stock_count = Product.objects.filter(stock_qty__lt=10).count()

    return DashboardStats(total_customers=total_customers, today_sales_revenue=today_revenue,
                           low_stock_alert=low_stock_count, generated_at=timezone.now())