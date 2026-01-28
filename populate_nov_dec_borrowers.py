#!/usr/bin/env python
import os
import sys
import django
from datetime import datetime, timedelta

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "supply_.settings")
django.setup()

from inventory.models import User, Supply, BorrowedItem
from django.utils import timezone


def populate_nov_dec_borrowers():
    print("Populating borrowed items for Clark, Jess, Ann, Marie (Nov-Dec 2025)...")

    borrower_names = ["Clark", "Jess", "Ann", "Marie"]
    borrowers = []

    for name in borrower_names:
        user, created = User.objects.get_or_create(
            username=name.lower(),
            defaults={
                "email": f"{name.lower()}@example.com",
                "role": "department_user",
                "department": "Test Department",
                "approval_status": "approved",
                "is_active": True,
            },
        )
        if created:
            user.set_password("password123")
            user.save()
            print(f"Created user: {name.lower()} / password123")
        else:
            print(f"User already exists: {name.lower()}")
        borrowers.append(user)

    supplies = list(Supply.objects.all()[:5])
    if not supplies:
        print("No supply items found. Please create supply items first.")
        return

    print(f"\nUsing {len(supplies)} supply items for borrowing records...")

    start_date = datetime(2025, 11, 1).date()
    end_date = datetime(2025, 12, 31).date()

    borrowed_items_data = [
        {
            "name": "Clark",
            "days_borrowed_ago": 65,
            "days_until_due": -10,
            "returned": False,
        },  # Overdue
        {
            "name": "Clark",
            "days_borrowed_ago": 55,
            "days_until_due": -20,
            "returned": True,
        },  # Returned, was overdue
        {
            "name": "Jess",
            "days_borrowed_ago": 70,
            "days_until_due": -15,
            "returned": False,
        },  # Overdue
        {
            "name": "Jess",
            "days_borrowed_ago": 40,
            "days_until_due": -5,
            "returned": True,
        },  # Returned
        {
            "name": "Ann",
            "days_borrowed_ago": 60,
            "days_until_due": -8,
            "returned": False,
        },  # Overdue
        {
            "name": "Ann",
            "days_borrowed_ago": 30,
            "days_until_due": 2,
            "returned": False,
        },  # Not overdue yet
        {
            "name": "Marie",
            "days_borrowed_ago": 75,
            "days_until_due": -20,
            "returned": False,
        },  # Overdue
        {
            "name": "Marie",
            "days_borrowed_ago": 50,
            "days_until_due": -12,
            "returned": True,
        },  # Returned
        {
            "name": "Clark",
            "days_borrowed_ago": 45,
            "days_until_due": -3,
            "returned": False,
        },  # Overdue
        {
            "name": "Jess",
            "days_borrowed_ago": 35,
            "days_until_due": 5,
            "returned": False,
        },  # Not overdue
    ]

    created_count = 0
    for i, data in enumerate(borrowed_items_data):
        borrower = User.objects.get(username=data["name"].lower())
        supply = supplies[i % len(supplies)]

        today = timezone.now().date()
        borrowed_date = today - timedelta(days=data["days_borrowed_ago"])
        return_deadline = borrowed_date + timedelta(
            days=data["days_until_due"] + data["days_borrowed_ago"]
        )

        returned_at = None
        if data["returned"]:
            returned_at = timezone.now() - timedelta(
                days=data["days_borrowed_ago"] - 10
            )

        borrowed_item, created = BorrowedItem.objects.get_or_create(
            supply=supply,
            borrower=borrower,
            borrowed_date=borrowed_date,
            defaults={
                "borrowed_quantity": 1,
                "return_deadline": return_deadline,
                "returned_at": returned_at,
                "location_when_borrowed": "Main Office",
                "notes": f"Demo item borrowed by {data['name']} in Nov-Dec 2025",
            },
        )

        if created:
            created_count += 1
            status = (
                "Returned"
                if data["returned"]
                else ("OVERDUE" if borrowed_item.is_overdue else "Active")
            )
            print(f"  Created: {data['name']} borrowed {supply.name} - {status}")

    print(f"\nTotal borrowed items created: {created_count}")
    print("\nBorrowing records summary:")
    print("=" * 60)

    for name in borrower_names:
        user = User.objects.get(username=name.lower())
        items = BorrowedItem.objects.filter(borrower=user)
        overdue = items.filter(
            returned_at__isnull=True, return_deadline__lt=timezone.now().date()
        ).count()
        returned = items.filter(returned_at__isnull=False).count()
        active = items.filter(
            returned_at__isnull=True, return_deadline__gte=timezone.now().date()
        ).count()
        print(
            f"{name}: {items.count()} total | {overdue} overdue | {returned} returned | {active} active"
        )


if __name__ == "__main__":
    populate_nov_dec_borrowers()
