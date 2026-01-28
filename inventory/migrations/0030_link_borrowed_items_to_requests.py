# Generated data migration to link BorrowedItems to SupplyRequests

from django.db import migrations


def link_borrowed_items_to_requests(apps, schema_editor):
    """Link existing BorrowedItems to their matching SupplyRequests"""
    BorrowedItem = apps.get_model('inventory', 'BorrowedItem')
    SupplyRequest = apps.get_model('inventory', 'SupplyRequest')
    
    # Get all BorrowedItems without a supply_request
    items_without_request = BorrowedItem.objects.filter(supply_request__isnull=True)
    
    fixed_count = 0
    for bi in items_without_request:
        # Try to find matching SupplyRequest
        matching_requests = SupplyRequest.objects.filter(
            supply=bi.supply,
            user=bi.borrower,
            purpose__startswith='[BORROWING]',
            status__in=['released', 'partially_returned', 'returned', 'returned_with_issues']
        ).order_by('-created_at')
        
        if matching_requests.exists():
            bi.supply_request = matching_requests.first()
            bi.save()
            fixed_count += 1
    
    print(f"Linked {fixed_count} BorrowedItems to SupplyRequests")


def reverse_link(apps, schema_editor):
    """Reverse migration - do nothing"""
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0029_add_return_status_choices'),
    ]

    operations = [
        migrations.RunPython(link_borrowed_items_to_requests, reverse_link),
    ]
