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
from inventory.utils import has_overdue_items, get_user_overdue_items

def test_borrowing_restriction():
    """
    Test the borrowing restriction functionality
    """
    print("Testing borrowing restriction functionality...")
    
    # Get the department user we used for the demo
    try:
        department_user = User.objects.get(username='dept')
        print(f"Testing for user: {department_user.username}")
    except User.DoesNotExist:
        print("Department user 'dept' not found.")
        return
    
    # Check if the user has overdue items
    has_overdue = has_overdue_items(department_user)
    print(f"User has overdue items: {has_overdue}")
    
    if has_overdue:
        # Get the overdue items
        overdue_items = get_user_overdue_items(department_user)
        print(f"Number of overdue items: {overdue_items.count()}")
        
        # Display details of overdue items
        for item in overdue_items:
            print(f"  - {item.supply.name} (ID: {item.id})")
            print(f"    Due date: {item.return_deadline}")
            print(f"    Overdue by: {(timezone.now() - item.return_deadline).days} days")
    
    # Try to get a supply for borrowing
    supply = Supply.objects.first()
    if supply:
        print(f"\nTrying to create a borrowing request for: {supply.name}")
        print("This should be blocked in the UI because the user has overdue items.")
        print("In the request_borrow_item view, the user would be redirected with an error message.")
    else:
        print("No supply items available for testing.")

if __name__ == "__main__":
    from django.utils import timezone
    test_borrowing_restriction()