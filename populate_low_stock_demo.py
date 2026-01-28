#!/usr/bin/env python
import os
import sys
import django
from django.conf import settings

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'supply_.settings')
django.setup()

from django.contrib.auth import get_user_model
from inventory.models import SupplyCategory, Supply, User

def populate_low_stock_demo():
    """Populate the database with sample data that will trigger low stock alerts"""
    
    User = get_user_model()
    
    print("Populating database with low stock demo data...")
    
    # Create categories if they don't exist
    categories_data = [
        {"name": "Office Supplies", "description": "General office supplies"},
        {"name": "Electronics", "description": "Electronic devices and accessories"},
        {"name": "Furniture", "description": "Office furniture and equipment"},
        {"name": "Cleaning Supplies", "description": "Cleaning materials and equipment"},
    ]
    
    categories = []
    for cat_data in categories_data:
        category, created = SupplyCategory.objects.get_or_create(
            name=cat_data["name"],
            defaults=cat_data
        )
        categories.append(category)
        if created:
            print(f"Created category: {category.name}")
        else:
            print(f"Category already exists: {category.name}")
    
    # Create or get admin user
    admin_user, created = User.objects.get_or_create(
        username="admin",
        defaults={
            "email": "admin@example.com",
            "first_name": "Admin",
            "last_name": "User",
            "role": "admin",
            "approval_status": "approved",
            "is_staff": True,
            "is_superuser": True,
        }
    )
    if created:
        admin_user.set_password("admin123")
        admin_user.save()
        print("Created admin user: admin/admin123")
    else:
        print("Admin user already exists")
    
    # Create supplies with quantities just above or at minimum levels to demonstrate alerts
    supplies_data = [
        {
            "name": "Stapler",
            "description": "Standard office stapler",
            "category": categories[0],
            "quantity": 3,  # Below min_stock_level of 5 - will trigger alert
            "min_stock_level": 5,
            "unit": "pieces",
            "cost_per_unit": 15.99,
            "location": "Office Storage Room A"
        },
        {
            "name": "Notebooks",
            "description": "Spiral bound notebooks, 100 sheets",
            "category": categories[0],
            "quantity": 7,  # Just above min_stock_level of 5
            "min_stock_level": 5,
            "unit": "pieces",
            "cost_per_unit": 8.50,
            "location": "Office Storage Room B"
        },
        {
            "name": "USB-C Cable",
            "description": "2m USB-C to USB-C charging cable",
            "category": categories[1],
            "quantity": 2,  # Below min_stock_level of 5 - will trigger alert
            "min_stock_level": 5,
            "unit": "pieces",
            "cost_per_unit": 12.99,
            "location": "Electronics Cabinet"
        },
        {
            "name": "Whiteboard Markers",
            "description": "Assorted color whiteboard markers",
            "category": categories[0],
            "quantity": 4,  # Below min_stock_level of 5 - will trigger alert
            "min_stock_level": 5,
            "unit": "set",
            "cost_per_unit": 24.99,
            "location": "Conference Room"
        },
        {
            "name": "Paper Clips",
            "description": "Standard paper clips, 100 count box",
            "category": categories[0],
            "quantity": 6,  # Just above min_stock_level of 5
            "min_stock_level": 5,
            "unit": "box",
            "cost_per_unit": 3.99,
            "location": "Office Storage Room A"
        }
    ]
    
    supplies = []
    for supply_data in supplies_data:
        supply, created = Supply.objects.get_or_create(
            name=supply_data["name"],
            defaults=supply_data
        )
        if not created:
            # Update existing supply with our test data
            for key, value in supply_data.items():
                setattr(supply, key, value)
            supply.save()
        supplies.append(supply)
        print(f"{'Created' if created else 'Updated'} supply: {supply.name} (Qty: {supply.quantity}, Min: {supply.min_stock_level})")
        
        # Generate QR code for the supply
        try:
            supply.generate_qr_code()
            print(f"  Generated QR code for {supply.name}")
        except Exception as e:
            print(f"  Failed to generate QR code for {supply.name}: {e}")
    
    # Summary
    low_stock_count = sum(1 for supply in supplies if supply.is_low_stock)
    print(f"\nSummary:")
    print(f"  - Created/updated {len(supplies)} supplies")
    print(f"  - {low_stock_count} supplies are currently at low stock levels")
    print(f"  - Login as admin/admin123 to see the low stock alerts in the dashboard and supply management pages")
    
    return supplies

if __name__ == "__main__":
    populate_low_stock_demo()