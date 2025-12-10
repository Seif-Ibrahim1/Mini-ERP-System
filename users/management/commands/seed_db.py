from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import transaction
from inventory.models import Product, StockMovementLog
from sales.models import Customer, Sequence, SalesOrder
from decimal import Decimal

User = get_user_model()

class Command(BaseCommand):
    help = 'seeds the database'

    def handle(self, *args, **kwargs):
        self.stdout.write("Seeding data... please wait.")
        
        with transaction.atomic():
            self.stdout.write("Cleaning old records...")
            SalesOrder.objects.all().delete()
            Customer.objects.all().delete()
            Product.objects.all().delete()
            User.objects.exclude(is_superuser=True).delete()
            Sequence.objects.all().delete()

            self.stdout.write("Creating Users...")
            if not User.objects.filter(username='admin').exists():
                User.objects.create_superuser('admin', 'admin@admin.com', 'admin123')
            
            karim = User.objects.create_user(
                username='karim',
                email='karim@jewelry.com',
                password='password123',
                role='SALES'
            )
            
            seif= User.objects.create_user(
                username='seif',
                email='seif@jewelry.com',
                password='password123',
                role='SALES'
            )

            self.stdout.write("Creating Inventory...")
            products = [
                Product(
                    sku='GLD-18K-R01', 
                    name='Gold Ring 18K (Lazurde Style)', 
                    category='Rings',
                    cost_price=Decimal('8000.00'), 
                    selling_price=Decimal('9500.00'), 
                    stock_qty=50
                ),
                Product(
                    sku='GLD-21K-N05', 
                    name='Heavy Gold Necklace 21K', 
                    category='Necklaces',
                    cost_price=Decimal('45000.00'), 
                    selling_price=Decimal('52000.00'), 
                    stock_qty=12
                ),
                Product(
                    sku='DIA-SOL-002', 
                    name='Diamond Solitaire Ring (VS1)', 
                    category='Diamonds',
                    cost_price=Decimal('75000.00'), 
                    selling_price=Decimal('120000.00'), 
                    stock_qty=5
                ),
                Product(
                    sku='SLV-ITA-925', 
                    name='Italian Silver Bracelet 925', 
                    category='Silver',
                    cost_price=Decimal('1200.00'), 
                    selling_price=Decimal('2500.00'), 
                    stock_qty=100
                ),
            ]
            Product.objects.bulk_create(products)

            self.stdout.write("Creating Customers...")
            customers = [
                Customer(
                    code='CUST-1001',
                    name='Hassan El-Shazly',
                    phone='01000000000',
                    address='12 El-Thawra St, Korba, Heliopolis, Cairo',
                    email='hassan.shazly@gmail.com',
                    opening_balance=Decimal('0.00')
                ),
                Customer(
                    code='CUST-1002',
                    name='Nourhan Mahmoud',
                    phone='01222222222',
                    address='Villa 45, Fifth Settlement, New Cairo',
                    email='nourhan.m@hotmail.com',
                    opening_balance=Decimal('0.00')
                ),
                Customer(
                    code='CUST-1003',
                    name='Tarek Youssef',
                    phone='01111111111',
                    address='7 Mohie El-Din St, Mohandessin, Giza',
                    email='tarek.joe@yahoo.com',
                    opening_balance=Decimal('0.00')
                ),
            ]
            Customer.objects.bulk_create(customers)
            Sequence.objects.create(key='sales_order', last_number=0)

        self.stdout.write(self.style.SUCCESS("database seeded successfully"))