"""
Demo data population script for Equipment Instance tracking feature.
Creates supplies with equipment instances and batch borrow requests.

Run with: uv run python populate_instance_demo.py
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'equipment_qr.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from django.utils import timezone
from inventory.models import (
    User, Supply, SupplyCategory, SupplyRequest, 
    EquipmentInstance, BorrowedItem
)

def main():
    print("=" * 60)
    print("Populating Equipment Instance Demo Data")
    print("=" * 60)
    
    # Get or create admin user
    admin = User.objects.filter(role='admin').first()
    if not admin:
        admin = User.objects.create_user(
            username='admin',
            email='admin@test.com',
            password='admin123',
            role='admin',
            approval_status='approved'
        )
        print(f"✓ Created admin user: {admin.username}")
    else:
        print(f"✓ Using existing admin: {admin.username}")
    
    # Get or create GSO staff
    gso = User.objects.filter(role='gso_staff').first()
    if not gso:
        gso = User.objects.create_user(
            username='gso_staff',
            email='gso@test.com',
            password='gso123',
            role='gso_staff',
            approval_status='approved'
        )
        print(f"✓ Created GSO staff: {gso.username}")
    else:
        print(f"✓ Using existing GSO: {gso.username}")
    
    # Get or create department user
    dept_user = User.objects.filter(role='department_user').first()
    if not dept_user:
        dept_user = User.objects.create_user(
            username='dept_user',
            email='dept@test.com',
            password='dept123',
            role='department_user',
            department='IT Department',
            approval_status='approved'
        )
        print(f"✓ Created department user: {dept_user.username}")
    else:
        print(f"✓ Using existing dept user: {dept_user.username}")
    
    # Get or create Equipment category
    category, _ = SupplyCategory.objects.get_or_create(
        name='Equipment',
        defaults={'description': 'Office equipment', 'is_material': False}
    )
    print(f"✓ Category: {category.name}")
    
    # Create supplies with equipment instances
    supplies_data = [
        {
            'name': 'Laptop',
            'description': 'Dell Latitude laptop for office use',
            'quantity': 5,
            'instances': [
                {'brand': 'Dell', 'model': 'Latitude 5520', 'serial': 'DELL-LAP-001'},
                {'brand': 'Dell', 'model': 'Latitude 5520', 'serial': 'DELL-LAP-002'},
                {'brand': 'Dell', 'model': 'Latitude 5520', 'serial': 'DELL-LAP-003'},
                {'brand': 'HP', 'model': 'EliteBook 840', 'serial': 'HP-LAP-004'},
                {'brand': 'HP', 'model': 'EliteBook 840', 'serial': 'HP-LAP-005'},
            ]
        },
        {
            'name': 'Aircon',
            'description': 'Portable air conditioning unit',
            'quantity': 3,
            'instances': [
                {'brand': 'Carrier', 'model': '1.5HP Split', 'serial': 'AC-001'},
                {'brand': 'Carrier', 'model': '1.5HP Split', 'serial': 'AC-002'},
                {'brand': 'Samsung', 'model': '2HP Window', 'serial': 'AC-003'},
            ]
        },
        {
            'name': 'Projector',
            'description': 'Epson HD Projector',
            'quantity': 2,
            'instances': [
                {'brand': 'Epson', 'model': 'EB-X51', 'serial': 'PROJ-001'},
                {'brand': 'Epson', 'model': 'EB-X51', 'serial': 'PROJ-002'},
            ]
        },
    ]
    
    created_supplies = []
    for supply_data in supplies_data:
        supply, created = Supply.objects.get_or_create(
            name=supply_data['name'],
            defaults={
                'description': supply_data['description'],
                'category': category,
                'quantity': supply_data['quantity'],
                'min_stock_level': 1,
                'unit': 'unit',
                'is_consumable': False,
            }
        )
        
        if created:
            supply.generate_qr_code()
            print(f"✓ Created supply: {supply.name}")
        else:
            print(f"✓ Using existing supply: {supply.name}")
        
        # Create instances
        prefix = supply.name[:3].upper()
        for idx, inst_data in enumerate(supply_data['instances'], 1):
            instance_code = f"{prefix}-{idx:03d}"
            instance, inst_created = EquipmentInstance.objects.get_or_create(
                instance_code=instance_code,
                defaults={
                    'supply': supply,
                    'brand': inst_data['brand'],
                    'model_name': inst_data['model'],
                    'serial_number': inst_data['serial'],
                    'status': 'available',
                }
            )
            if inst_created:
                instance.generate_qr_code()
                print(f"  ✓ Created instance: {instance.instance_code} ({inst_data['brand']} {inst_data['model']})")
        
        created_supplies.append(supply)
    
    # Create a pending batch borrow request
    print("\n--- Creating Batch Borrow Request ---")
    batch_timestamp = timezone.now()
    
    for supply in created_supplies[:2]:  # First 2 supplies
        qty = 2 if supply.quantity >= 2 else 1
        req, created = SupplyRequest.objects.get_or_create(
            user=dept_user,
            supply=supply,
            status='pending',
            defaults={
                'quantity_requested': qty,
                'purpose': f'[BORROWING] Need {supply.name} for project meeting',
                'requested_location': 'Conference Room A',
            }
        )
        if created:
            print(f"✓ Created pending borrow request: {supply.name} x{qty}")
    
    # Create an approved batch borrow request ready for issue
    print("\n--- Creating Approved Batch Request (Ready for Issue) ---")
    for supply in created_supplies[1:3]:  # 2nd and 3rd supplies
        qty = 1
        existing = SupplyRequest.objects.filter(
            user=dept_user,
            supply=supply,
            status='approved'
        ).first()
        
        if not existing:
            req = SupplyRequest.objects.create(
                user=dept_user,
                supply=supply,
                quantity_requested=qty,
                purpose='[BORROWING] Department event setup',
                requested_location='Main Hall',
                status='approved',
                approved_by=gso,
                approved_at=timezone.now(),
            )
            req.generate_batch_qr_code()
            print(f"✓ Created APPROVED request: {supply.name} x{qty} (Ready for QR issue)")
    
    print("\n" + "=" * 60)
    print("Demo Data Population Complete!")
    print("=" * 60)
    print("\nTest Accounts:")
    print("  Admin:     admin / admin123")
    print("  GSO Staff: gso_staff / gso123") 
    print("  Dept User: dept_user / dept123")
    print("\nNext Steps:")
    print("  1. Login as dept_user and go to 'Request to Borrow' page")
    print("  2. You can also approve pending requests as gso_staff")
    print("  3. Scan the batch QR code to issue items (instances auto-assign)")
    print("  4. Go to a supply -> 'Instances' to see created instances")
    print("=" * 60)

if __name__ == '__main__':
    main()
