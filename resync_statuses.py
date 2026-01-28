
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'equip.settings')
django.setup()

from inventory.models import SupplyRequest, BorrowedItem

print("Re-syncing all SupplyRequests statuses based on BorrowedItems...")
count = 0
for sr in SupplyRequest.objects.filter(status__in=['released', 'partially_returned', 'returned', 'returned_with_issues']):
    all_items = BorrowedItem.objects.filter(supply_request=sr)
    if all_items.exists():
        unreturned = all_items.filter(returned_at__isnull=True)
        if not unreturned.exists():
            # All items returned
            has_issues = all_items.filter(return_status__in=['damaged', 'lost']).exists()
            new_status = 'returned_with_issues' if has_issues else 'returned'
            if sr.status != new_status:
                print(f"  SR {sr.request_id}: {sr.status} -> {new_status}")
                sr.status = new_status
                sr.save()
                count += 1
        elif all_items.filter(returned_at__isnull=False).exists():
            # Partially returned
            if sr.status != 'partially_returned':
                print(f"  SR {sr.request_id}: {sr.status} -> partially_returned")
                sr.status = 'partially_returned'
                sr.save()
                count += 1

print(f"Successfully re-synced {count} requests.")
