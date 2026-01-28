#!/usr/bin/env python
import os
import sys
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'supply_.settings')
django.setup()

from django.contrib.auth.hashers import make_password
from inventory.models import User, SupplyCategory, Supply, SupplyRequest

def setup_demo_data():
    print("Setting up demo data...")
    
    # Create or update admin user
    try:
        admin = User.objects.get(username='admin')
        print("Admin user found, updating...")
    except User.DoesNotExist:
        admin = User(username='admin')
        print("Admin user created...")
    
    admin.first_name = 'System'
    admin.last_name = 'Administrator'
    admin.role = 'admin'
    admin.department = 'IT Department'
    admin.set_password('password123')
    admin.save()
    
    # Create GSO Staff user
    try:
        gso = User.objects.get(username='gso')
        print("GSO user found, updating...")
    except User.DoesNotExist:
        gso = User.objects.create(
            username='gso',
            email='gso@jhcsc.edu.ph',
            first_name='GSO',
            last_name='Staff',
            role='gso_staff',
            department='General Services Office'
        )
        print("GSO user created...")
    
    gso.set_password('password123')
    gso.save()
    
    # Create Department User
    try:
        dept = User.objects.get(username='dept')
        print("Department user found, updating...")
    except User.DoesNotExist:
        dept = User.objects.create(
            username='dept',
            email='dept@jhcsc.edu.ph',
            first_name='Department',
            last_name='User',
            role='department_user',
            department='Academic Department'
        )
        print("Department user created...")
    
    dept.set_password('password123')
    dept.save()
    
    # Create supply categories
    category_names = ['Office Supplies', 'IT Equipment', 'Cleaning Supplies', 'Educational Materials', 'Furniture']
    categories = []
    
    for name in category_names:
        category, created = SupplyCategory.objects.get_or_create(
            name=name,
            defaults={
                'description': f'Description for {name}'
            }
        )
        if created:
            print(f"Created category: {name}")
        categories.append(category)
    
    # Update category descriptions
    category_updates = [
        ('Office Supplies', 'General office supplies and materials'),
        ('IT Equipment', 'Computer and technology related supplies'),
        ('Cleaning Supplies', 'Cleaning and maintenance materials'),
        ('Educational Materials', 'Teaching and learning materials'),
        ('Furniture', 'Office and classroom furniture'),
    ]
    
    for name, description in category_updates:
        try:
            category = SupplyCategory.objects.get(name=name)
            category.description = description
            category.save()
        except SupplyCategory.DoesNotExist:
            pass
    
    # Create sample supplies
    supplies_data = [
        {
            'name': 'A4 Printer Paper',
            'description': 'Standard A4 size printer paper, 80gsm, white',
            'category': categories[0],
            'quantity': 50,
            'min_stock_level': 10,
            'unit': 'reams',
            'cost_per_unit': 250.00,
            'location': 'Main Storage'
        },
        {
            'name': 'Ballpen Black',
            'description': 'Black ink ballpen, medium point',
            'category': categories[0],
            'quantity': 200,
            'min_stock_level': 50,
            'unit': 'pieces',
            'cost_per_unit': 15.00,
            'location': 'Main Storage'
        },
        {
            'name': 'Ballpen Blue',
            'description': 'Blue ink ballpen, medium point',
            'category': categories[0],
            'quantity': 150,
            'min_stock_level': 50,
            'unit': 'pieces',
            'cost_per_unit': 15.00,
            'location': 'Main Storage'
        },
        {
            'name': 'Stapler',
            'description': 'Standard office stapler',
            'category': categories[0],
            'quantity': 25,
            'min_stock_level': 5,
            'unit': 'pieces',
            'cost_per_unit': 120.00,
            'location': 'Main Storage'
        },
        {
            'name': 'Staples',
            'description': 'Standard staples for office stapler',
            'category': categories[0],
            'quantity': 100,
            'min_stock_level': 20,
            'unit': 'boxes',
            'cost_per_unit': 25.00,
            'location': 'Main Storage'
        },
        {
            'name': 'USB Flash Drive 32GB',
            'description': '32GB USB 3.0 flash drive',
            'category': categories[1],
            'quantity': 30,
            'min_stock_level': 10,
            'unit': 'pieces',
            'cost_per_unit': 450.00,
            'location': 'IT Storage'
        },
        {
            'name': 'Wireless Mouse',
            'description': 'Wireless optical mouse with USB receiver',
            'category': categories[1],
            'quantity': 15,
            'min_stock_level': 5,
            'unit': 'pieces',
            'cost_per_unit': 350.00,
            'location': 'IT Storage'
        },
        {
            'name': 'Keyboard',
            'description': 'Standard USB keyboard',
            'category': categories[1],
            'quantity': 10,
            'min_stock_level': 5,
            'unit': 'pieces',
            'cost_per_unit': 500.00,
            'location': 'IT Storage'
        },
        {
            'name': 'Disinfectant Spray',
            'description': 'Multi-purpose disinfectant spray, 500ml',
            'category': categories[2],
            'quantity': 8,
            'min_stock_level': 5,
            'unit': 'bottles',
            'cost_per_unit': 180.00,
            'location': 'Cleaning Storage'
        },
        {
            'name': 'Floor Wax',
            'description': 'Floor wax polish, 1 gallon',
            'category': categories[2],
            'quantity': 3,
            'min_stock_level': 2,
            'unit': 'gallons',
            'cost_per_unit': 350.00,
            'location': 'Cleaning Storage'
        },
    ]
    
    # Create or update supplies
    for supply_data in supplies_data:
        supply, created = Supply.objects.get_or_create(
            name=supply_data['name'],
            defaults=supply_data
        )
        if created:
            print(f"Created supply: {supply_data['name']}")
            supply.generate_qr_code()  # Generate QR code
        else:
            print(f"Supply already exists: {supply_data['name']}")
    
    # Create sample requests
    requests_data = [
        {
            'user': dept,
            'supply': Supply.objects.get(name='A4 Printer Paper'),
            'quantity_requested': 5,
            'purpose': 'For printing examination papers and handouts'
        },
        {
            'user': dept,
            'supply': Supply.objects.get(name='Ballpen Black'),
            'quantity_requested': 20,
            'purpose': 'For faculty use and student activities'
        },
        {
            'user': dept,
            'supply': Supply.objects.get(name='USB Flash Drive 32GB'),
            'quantity_requested': 3,
            'purpose': 'For faculty data storage and backup'
        }
    ]
    
    # Create requests
    for request_data in requests_data:
        # Check if request already exists to avoid duplicates
        existing_request = SupplyRequest.objects.filter(
            user=request_data['user'],
            supply=request_data['supply'],
            quantity_requested=request_data['quantity_requested']
        ).first()
        
        if not existing_request:
            request = SupplyRequest(**request_data)
            request.save()
            print(f"Created request for {request_data['supply'].name}")
        else:
            print(f"Request already exists for {request_data['supply'].name}")
    
    print("Demo data setup completed successfully!")
    print("\nDemo Accounts:")
    print("Admin: admin / password123")
    print("GSO Staff: gso / password123")
    print("Department User: dept / password123")

if __name__ == '__main__':
    setup_demo_data()