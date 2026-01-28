"""
Demo data population command for Equipment Instance tracking feature.
Creates supplies with equipment instances and batch borrow requests.

Run with: uv run python manage.py populate_instance_demo
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from inventory.models import (
    User, Supply, SupplyCategory, SupplyRequest, 
    EquipmentInstance, BorrowedItem
)


class Command(BaseCommand):
    help = 'Populate demo data for equipment instance tracking'

    def handle(self, *args, **options):
        self.stdout.write("=" * 60)
        self.stdout.write("Populating Equipment Instance Demo Data")
        self.stdout.write("=" * 60)
        
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
            self.stdout.write(self.style.SUCCESS(f"Created admin user: {admin.username}"))
        else:
            self.stdout.write(f"Using existing admin: {admin.username}")
        
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
            self.stdout.write(self.style.SUCCESS(f"Created GSO staff: {gso.username}"))
        else:
            self.stdout.write(f"Using existing GSO: {gso.username}")
        
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
            self.stdout.write(self.style.SUCCESS(f"Created department user: {dept_user.username}"))
        else:
            self.stdout.write(f"Using existing dept user: {dept_user.username}")
        
        # Get or create Equipment category
        category, _ = SupplyCategory.objects.get_or_create(
            name='Equipment',
            defaults={'description': 'Office equipment', 'is_material': False}
        )
        self.stdout.write(f"Category: {category.name}")
        
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
                self.stdout.write(self.style.SUCCESS(f"Created supply: {supply.name}"))
            else:
                self.stdout.write(f"Using existing supply: {supply.name}")
            
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
                    self.stdout.write(f"  Created instance: {instance.instance_code} ({inst_data['brand']} {inst_data['model']})")
            
            created_supplies.append(supply)
        
        # Create a pending batch borrow request
        self.stdout.write("\n--- Creating Batch Borrow Request ---")
        
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
                self.stdout.write(self.style.SUCCESS(f"Created pending borrow request: {supply.name} x{qty}"))
        
        # Create an approved batch borrow request ready for issue
        self.stdout.write("\n--- Creating Approved Batch Request (Ready for Issue) ---")
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
                req.generate_borrowing_qr_code()
                self.stdout.write(self.style.SUCCESS(f"Created APPROVED request: {supply.name} x{qty} (Ready for QR issue)"))
        
        self.stdout.write("\n" + "=" * 60)
        self.stdout.write(self.style.SUCCESS("Demo Data Population Complete!"))
        self.stdout.write("=" * 60)
        self.stdout.write("\nTest Accounts:")
        self.stdout.write("  Admin:     admin / admin123")
        self.stdout.write("  GSO Staff: gso_staff / gso123") 
        self.stdout.write("  Dept User: dept_user / dept123")
        self.stdout.write("\nNext Steps:")
        self.stdout.write("  1. Login as dept_user and go to 'Request to Borrow' page")
        self.stdout.write("  2. You can also approve pending requests as gso_staff")
        self.stdout.write("  3. Scan the batch QR code to issue items (instances auto-assign)")
        self.stdout.write("  4. Go to a supply -> 'Instances' to see created instances")
        self.stdout.write("=" * 60)
