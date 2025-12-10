from dataclasses import dataclass
from decimal import Decimal
from datetime import datetime

@dataclass
class DashboardStats:
    total_customers: int
    today_sales_revenue: Decimal
    low_stock_alert: int
    generated_at: datetime