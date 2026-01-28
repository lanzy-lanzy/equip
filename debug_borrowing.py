#!/usr/bin/env python
import os
import sys
import django

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'supply_.settings')
django.setup()

from inventory.models import User, Supply, SupplyRequest, BorrowedItem
from inventory.utils import has_overdue_items, get_user_overdue_items
from django.utils import timezone

def debug_borrowing():
    """
    Debug the borrowing request process
    """
    print("Debugging borrowing request process...")
    print("=" * 50)
    
    # Get the department user
    try:
        dept_user = User.objects.get(username='dept')
        print(f"User: {dept_user.username} (ID: {dept_user.id})")
        print(f"Role: {dept_user.role}")
    except User.DoesNotExist:
        print("User 'dept' not found.")
        return
    
    # Check if user has overdue items
    print("\nChecking for overdue items:")
    has_overdue = has_overdue_items(dept_user)
    print(f"  has_overdue_items() result: {has_overdue}")
    
    if has_overdue:
        overdue_items = get_user_overdue_items(dept_user)
        print(f"  Number of overdue items: {overdue_items.count()}")
        for item in overdue_items:
            print(f"    - {item.supply.name} (ID: {item.id})")
            print(f"      Due: {item.return_deadline}")
            print(f"      Overdue by: {(timezone.now() - item.return_deadline).days} days")
    
    # Check if there are supplies available
    print("\nChecking available supplies:")
    available_supplies = Supply.objects.filter(quantity__gt=0)
    print(f"  Available supplies: {available_supplies.count()}")
    for supply in available_supplies[:3]:  # Show first 3
        print(f"    - {supply.name} (ID: {supply.id}, Quantity: {supply.quantity})")
    
    # Check existing requests
    print("\nChecking existing requests for this user:")
    user_requests = SupplyRequest.objects.filter(user=dept_user)
    print(f"  Total requests: {user_requests.count()}")
    for req in user_requests[:3]:  # Show first 3
        print(f"    - {req.supply.name} (ID: {req.id}, Status: {req.status})")

if __name__ == "__main__":
    debug_borrowing()