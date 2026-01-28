#!/usr/bin/env python
import os
import sys
import django

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'supply_.settings')
django.setup()

from inventory.models import User, Supply, BorrowedItem
from django.utils import timezone
from datetime import timedelta

def check_borrowed_items():
    """
    Check all borrowed items and their status
    """
    print("Checking all borrowed items...")
    print("=" * 50)
    
    borrowed_items = BorrowedItem.objects.all().select_related('supply', 'borrower')
    
    if not borrowed_items.exists():
        print("No borrowed items found in the database.")
        return
    
    for item in borrowed_items:
        print(f"Item ID: {item.id}")
        print(f"  Supply: {item.supply.name}")
        print(f"  Borrower: {item.borrower.username} (Role: {item.borrower.role})")
        print(f"  Borrowed at: {item.borrowed_at}")
        print(f"  Return deadline: {item.return_deadline}")
        print(f"  Returned at: {item.returned_at}")
        print(f"  Is returned: {item.is_returned}")
        print(f"  Is overdue: {item.is_overdue}")
        print(f"  Due status: {item.due_status}")
        if not item.is_returned and item.return_deadline:
            print(f"  Days until due (floor): {item.days_until_due}")
            print(f"  Due in (days, fractional): {item.due_in_days}")
        print(f"  Duration (human): {item.duration_display}")
        print("-" * 30)
    
    # Check specifically for the 'dept' user
    try:
        dept_user = User.objects.get(username='dept')
        print(f"\nChecking overdue items for user '{dept_user.username}':")
        user_items = BorrowedItem.objects.filter(borrower=dept_user)
        
        overdue_items = user_items.filter(
            returned_at__isnull=True,
            return_deadline__isnull=False,
            return_deadline__lt=timezone.now()
        )
        
        print(f"  Total borrowed items: {user_items.count()}")
        print(f"  Overdue items: {overdue_items.count()}")
        
        for item in overdue_items:
            print(f"    - {item.supply.name} (ID: {item.id})")
            print(f"      Due: {item.return_deadline}")
            print(f"      Overdue by: {(timezone.now() - item.return_deadline)}")
            
    except User.DoesNotExist:
        print(f"\nUser 'dept' not found.")

if __name__ == "__main__":
    check_borrowed_items()