
import os
import django
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'equip.settings')
django.setup()

from inventory.models import InventoryTransaction

print("Healing miscategorized return transactions for Jan 28...")

# Find 'adjustment' transactions from today with 0 quantity that were actually returns
today = timezone.now().date()
txs = InventoryTransaction.objects.filter(
    transaction_type='adjustment',
    quantity=0,
    created_at__year=today.year,
    created_at__month=today.month,
    created_at__day=today.day,
    reason__icontains='returned as'
)

print(f"Found {txs.count()} transactions to repair.")

count = 0
for t in txs:
    old_type = t.transaction_type
    old_reason = t.reason
    
    if 'returned as damaged' in old_reason.lower():
        t.transaction_type = 'damaged'
    elif 'returned as lost' in old_reason.lower():
        t.transaction_type = 'lost'
    else:
        continue
        
    t.quantity = -1
    # Update reason to cleaner format if possible
    t.reason = old_reason.replace('returned as', 'marked as').replace('Item', 'Marked') + " (Repaired)"
    t.save()
    print(f"  Repaired TX {t.id}: {old_type} -> {t.transaction_type}, reason: {t.reason}")
    count += 1

print(f"Successfully healed {count} transactions.")
