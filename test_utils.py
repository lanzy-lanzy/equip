#!/usr/bin/env python
import os
import sys
import django

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'supply_.settings')
django.setup()

from inventory.models import User
from inventory.utils import has_overdue_items, get_user_overdue_items
from django.utils import timezone

def test_utils():
    """
    Test the utility functions for overdue items
    """
    print("Testing overdue item utility functions...")
    print("=" * 50)
    
    # Get the department user
    try:
        dept_user = User.objects.get(username='dept')
        print(f"Testing for user: {dept_user.username} (ID: {dept_user.id})")
        print(f"User role: {dept_user.role}")
    except User.DoesNotExist:
        print("User 'dept' not found.")
        return
    
    # Test has_overdue_items function
    print("\nTesting has_overdue_items() function:")
    has_overdue = has_overdue_items(dept_user)
    print(f"  Result: {has_overdue}")
    
    # Test get_user_overdue_items function
    print("\nTesting get_user_overdue_items() function:")
    overdue_items = get_user_overdue_items(dept_user)
    print(f"  Number of overdue items: {overdue_items.count()}")
    
    # Display details
    for item in overdue_items:
        print(f"    - {item.supply.name} (ID: {item.id})")
        print(f"      Borrowed: {item.borrowed_at}")
        print(f"      Due: {item.return_deadline}")
        print(f"      Overdue by: {(timezone.now() - item.return_deadline).days} days")
    
    # Manual check using the same logic as has_overdue_items
    print("\nManual check using the same logic:")
    manual_check = dept_user.borrowed_items.filter(
        returned_at__isnull=True,
        return_deadline__isnull=False,
        return_deadline__lt=timezone.now()
    ).exists()
    print(f"  Manual check result: {manual_check}")

if __name__ == "__main__":
    test_utils()