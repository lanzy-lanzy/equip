#!/usr/bin/env python
import os
import sys
import django
from django.utils import timezone
from datetime import timedelta

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'supply_.settings')
django.setup()

from inventory.models import User, Supply, BorrowedItem, SupplyRequest, SupplyCategory

def populate_overdue_demo_data():
    """
    Populate sample data for testing overdue item functionality
    """
    print("Populating overdue demo data...")
    
    # Get a department user (or create one if none exists)
    try:
        department_user = User.objects.filter(role='department_user').first()
        if not department_user:
            print("No department user found. Please create a department user first.")
            return
        print(f"Using department user: {department_user.username}")
    except Exception as e:
        print(f"Error getting department user: {e}")
        return
    
    # Get or create multiple supply items
    supplies = []
    try:
        # Get existing non-consumable supplies first
        existing_supplies = list(Supply.objects.filter(is_consumable=False)[:5])
        supplies.extend(existing_supplies)
        
        # Create more if needed
        if len(supplies) < 5:
            category, _ = SupplyCategory.objects.get_or_create(name="Demo Equipment")
            for i in range(len(supplies), 5):
                new_supply = Supply.objects.create(
                    name=f"Demo Item {i+1}",
                    description=f"Description for demo item {i+1}",
                    category=category,
                    quantity=10,
                    min_stock_level=2,
                    is_consumable=False,
                    location="Demo Storage"
                )
                supplies.append(new_supply)
                print(f"Created new supply: {new_supply.name}")
        
        print(f"Using {len(supplies)} different supply items")
    except Exception as e:
        print(f"Error getting/creating supply items: {e}")
        return
    
    # Create 5 overdue borrowed items
    print("Creating 5 overdue items...")
    for i in range(1, 6):
        try:
            # Select supply (cycle through available supplies)
            supply = supplies[(i-1) % len(supplies)]
            
            days_overdue = i + 1  # 2, 3, 4, 5, 6 days overdue
            overdue_item = BorrowedItem.objects.create(
                supply=supply,
                borrower=department_user,
                borrowed_quantity=1,
                borrowed_date=timezone.now().date() - timedelta(days=days_overdue + 3), # Borrowed a few days before due
                location_when_borrowed="Main Office",
                notes=f"Demo overdue item #{i} for testing",
                return_deadline=timezone.now().date() - timedelta(days=days_overdue)
            )
            
            # Create corresponding SupplyRequest with QR code
            request_overdue = SupplyRequest.objects.create(
                user=department_user,
                supply=supply,
                quantity_requested=1,
                purpose=f"[BORROWING] Demo overdue item #{i} for testing",
                status='released',
                approved_at=timezone.now(),
                released_at=timezone.now()
            )
            request_overdue.generate_borrowing_qr_code()
            
            print(f"Created overdue item #{i}: {overdue_item.supply.name} (ID: {overdue_item.id})")
            print(f"  - Return deadline: {overdue_item.return_deadline}")
            print(f"  - Is overdue: {overdue_item.is_overdue}")
            print(f"  - QR Code generated: {request_overdue.borrowing_qr_code.name}")
        except Exception as e:
            print(f"Error creating overdue item #{i}: {e}")
    
    # Create a due soon borrowed item (due tomorrow)
    try:
        due_soon_item = BorrowedItem.objects.create(
            supply=supply,
            borrower=department_user,
            borrowed_quantity=1,
            borrowed_date=timezone.now().date() - timedelta(days=2),
            location_when_borrowed="Storage Room",
            notes="Demo item due soon for testing",
            return_deadline=timezone.now().date() + timedelta(days=1)  # Due tomorrow
        )
        
        # Create corresponding SupplyRequest with QR code
        request_due_soon = SupplyRequest.objects.create(
            user=department_user,
            supply=supply,
            quantity_requested=1,
            purpose="[BORROWING] Demo item due soon for testing",
            status='released',
            approved_at=timezone.now(),
            released_at=timezone.now()
        )
        request_due_soon.generate_borrowing_qr_code()
        
        print(f"Created due soon item: {due_soon_item.supply.name} (ID: {due_soon_item.id})")
        print(f"  - Borrowed by: {due_soon_item.borrower.username}")
        print(f"  - Return deadline: {due_soon_item.return_deadline}")
        print(f"  - Days until due: {due_soon_item.days_until_due}")
        print(f"  - QR Code generated: {request_due_soon.borrowing_qr_code.name}")
    except Exception as e:
        print(f"Error creating due soon item: {e}")
        return
    
    # Create a returned item (should not be considered overdue)
    try:
        returned_item = BorrowedItem.objects.create(
            supply=supply,
            borrower=department_user,
            borrowed_quantity=1,
            borrowed_date=timezone.now().date() - timedelta(days=4),
            location_when_borrowed="Reception",
            location_when_returned="Storage",
            returned_at=timezone.now() - timedelta(days=1),  # Returned 1 day ago
            notes="Demo returned item for testing",
            return_deadline=timezone.now().date() + timedelta(days=3)  # Was due in future
        )
        
        # Create corresponding SupplyRequest with QR code
        request_returned = SupplyRequest.objects.create(
            user=department_user,
            supply=supply,
            quantity_requested=1,
            purpose="[BORROWING] Demo returned item for testing",
            status='released',
            approved_at=timezone.now() - timedelta(days=4), # matched borrow date roughly
            released_at=timezone.now() - timedelta(days=4)
        )
        request_returned.generate_borrowing_qr_code()
        
        print(f"Created returned item: {returned_item.supply.name} (ID: {returned_item.id})")
        print(f"  - Borrowed by: {returned_item.borrower.username}")
        print(f"  - Returned at: {returned_item.returned_at}")
        print(f"  - Return deadline: {returned_item.return_deadline}")
        print(f"  - Is returned: {returned_item.is_returned}")
        print(f"  - Is overdue: {returned_item.is_overdue}")
        print(f"  - QR Code generated: {request_returned.borrowing_qr_code.name}")
    except Exception as e:
        print(f"Error creating returned item: {e}")
        return
    
    print("\nDemo data populated successfully!")
    print("You can now test the overdue item functionality:")
    print("1. Log in as the department user")
    print("2. Check the dashboard for overdue alerts")
    print("3. Try to borrow a new item (should be blocked due to overdue items)")
    print("4. Run the check_overdue_items management command to see alerts")

if __name__ == "__main__":
    populate_overdue_demo_data()