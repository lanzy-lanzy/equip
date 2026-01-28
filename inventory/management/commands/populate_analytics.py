"""
Management command to populate analytics for existing data
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.db.models import Count, Q
from inventory.models import (
    User, SupplyRequest, BorrowedItem,
    RequestorBorrowerAnalytics, UserActivityLog, MostRequestedItem
)


class Command(BaseCommand):
    help = 'Populate analytics records for existing requests and borrows'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting analytics population...'))
        
        # Create analytics records for all department users
        department_users = User.objects.filter(role='department_user')
        for user in department_users:
            analytics, created = RequestorBorrowerAnalytics.objects.get_or_create(user=user)
            
            # Count requests
            total_requests = SupplyRequest.objects.filter(user=user).count()
            approved_requests = SupplyRequest.objects.filter(user=user, status__in=['approved', 'released']).count()
            rejected_requests = SupplyRequest.objects.filter(user=user, status='rejected').count()
            
            # Count borrows
            total_borrowings = BorrowedItem.objects.filter(borrower=user).count()
            returned_items = BorrowedItem.objects.filter(borrower=user, returned_at__isnull=False).count()
            overdue_items = BorrowedItem.objects.filter(
                borrower=user,
                returned_at__isnull=True,
                return_deadline__lt=timezone.now().date()
            ).count()
            
            # Get last dates
            last_request = SupplyRequest.objects.filter(user=user).order_by('-created_at').first()
            last_borrow = BorrowedItem.objects.filter(borrower=user).order_by('-borrowed_at').first()
            
            # Update analytics
            analytics.total_requests = total_requests
            analytics.approved_requests = approved_requests
            analytics.rejected_requests = rejected_requests
            analytics.total_borrowings = total_borrowings
            analytics.returned_items = returned_items
            analytics.overdue_items = overdue_items
            analytics.last_request_date = last_request.created_at if last_request else None
            analytics.last_borrow_date = last_borrow.borrowed_at if last_borrow else None
            analytics.save()
            
            self.stdout.write(f'  Updated analytics for {user.username}')
        
        # Create most requested items
        supplies = {}
        
        # Get request stats
        request_stats = SupplyRequest.objects.values('supply_id').annotate(count=Count('supply_id'))
        for stat in request_stats:
            supply_id = stat['supply_id']
            if supply_id not in supplies:
                supplies[supply_id] = {'request_count': 0, 'borrow_count': 0}
            supplies[supply_id]['request_count'] = stat['count']
        
        # Get borrow stats
        borrow_stats = BorrowedItem.objects.values('supply_id').annotate(count=Count('supply_id'))
        for stat in borrow_stats:
            supply_id = stat['supply_id']
            if supply_id not in supplies:
                supplies[supply_id] = {'request_count': 0, 'borrow_count': 0}
            supplies[supply_id]['borrow_count'] = stat['count']
        
        # Update most requested items
        for supply_id, stats in supplies.items():
            most_requested, created = MostRequestedItem.objects.get_or_create(supply_id=supply_id)
            most_requested.request_count = stats['request_count']
            most_requested.borrow_count = stats['borrow_count']
            
            # Get last request/borrow times
            last_request = SupplyRequest.objects.filter(supply_id=supply_id).order_by('-created_at').first()
            last_borrow = BorrowedItem.objects.filter(supply_id=supply_id).order_by('-borrowed_at').first()
            
            most_requested.last_requested = last_request.created_at if last_request else None
            most_requested.last_borrowed = last_borrow.borrowed_at if last_borrow else None
            most_requested.save()
            
            self.stdout.write(f'  Updated most requested for supply {supply_id}')
        
        # Create activity logs from existing data
        existing_logs = UserActivityLog.objects.exists()
        if not existing_logs:
            self.stdout.write('Creating activity logs...')
            
            # From requests
            requests = SupplyRequest.objects.all()
            for req in requests:
                UserActivityLog.objects.create(
                    user=req.user,
                    activity_type='request',
                    supply=req.supply,
                    quantity=req.quantity_requested,
                    description=req.purpose[:100],
                    timestamp=req.created_at
                )
            
            # From borrows
            borrows = BorrowedItem.objects.all()
            for borrow in borrows:
                UserActivityLog.objects.create(
                    user=borrow.borrower,
                    activity_type='borrow',
                    supply=borrow.supply,
                    quantity=borrow.borrowed_quantity,
                    description=f'Borrowed until {borrow.return_deadline}',
                    timestamp=borrow.borrowed_at
                )
                
                if borrow.returned_at:
                    UserActivityLog.objects.create(
                        user=borrow.borrower,
                        activity_type='return',
                        supply=borrow.supply,
                        quantity=borrow.borrowed_quantity,
                        description=f'Returned item',
                        timestamp=borrow.returned_at
                    )
            
            self.stdout.write(f'  Created {requests.count() + borrows.count() * 2} activity logs')
        
        self.stdout.write(self.style.SUCCESS('Analytics population completed!'))
