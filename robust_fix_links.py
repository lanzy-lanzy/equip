"""
Robust fix script to properly distribute BorrowedItems among SupplyRequests (1-to-1)
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'equip.settings')
django.setup()

from inventory.models import BorrowedItem, SupplyRequest, User, Supply

print("Starting robust data fix...")

# 1. First, clear the bad links from the previous migration (where multiple BIs linked to same SR)
# This will reset SRs with multiple links back to having zero links for better redistribution.
from django.db.models import Count
sr_with_duplicates = BorrowedItem.objects.values('supply_request').annotate(num_bi=Count('id')).filter(num_bi__gt=1, supply_request__isnull=False)
for entry in sr_with_duplicates:
    sr_id = entry['supply_request']
    print(f"Clearing duplicate links from SR {sr_id}")
    BorrowedItem.objects.filter(supply_request_id=sr_id).update(supply_request=None)

# 2. Distribute unlinked BorrowedItems to unlinked SupplyRequests
# We group by (User, Supply) to match them correctly
unlinked_bi_groups = BorrowedItem.objects.filter(supply_request__isnull=True).values('borrower', 'supply').distinct()

for group in unlinked_bi_groups:
    user_id = group['borrower']
    supply_id = group['supply']
    
    # Get unlinked BIs for this user+supply
    bis = list(BorrowedItem.objects.filter(borrower_id=user_id, supply_id=supply_id, supply_request__isnull=True).order_by('borrowed_at'))
    
    # Get matching SRs that are missing a link
    srs = list(SupplyRequest.objects.filter(
        user_id=user_id, 
        supply_id=supply_id, 
        purpose__startswith='[BORROWING]',
        status__in=['released', 'partially_returned', 'returned', 'returned_with_issues']
    ).exclude(id__in=BorrowedItem.objects.filter(supply_request__isnull=False).values('supply_request')).order_by('created_at'))
    
    print(f"User {user_id}, Supply {supply_id}: processing {len(bis)} BIs and {len(srs)} SRs")
    
    # Link 1-to-1 as far as we can
    for i in range(min(len(bis), len(srs))):
        bi = bis[i]
        sr = srs[i]
        bi.supply_request = sr
        bi.save()
        print(f"  Linked BI {bi.id} -> SR {sr.id} ({sr.request_id})")

print("\nRobust fix complete.")
