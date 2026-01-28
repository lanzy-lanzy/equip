"""
Django signals for automatic analytics tracking
"""
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from .models import (
    SupplyRequest, BorrowedItem, User,
    RequestorBorrowerAnalytics, UserActivityLog, MostRequestedItem
)


@receiver(post_save, sender=User)
def create_analytics_record(sender, instance, created, **kwargs):
    """Create analytics record when a new user is created"""
    if created and instance.role == 'department_user':
        RequestorBorrowerAnalytics.objects.get_or_create(user=instance)


@receiver(post_save, sender=SupplyRequest)
def track_request_activity(sender, instance, created, **kwargs):
    """Track supply request activity"""
    if created:
        # Update analytics
        analytics, _ = RequestorBorrowerAnalytics.objects.get_or_create(user=instance.user)
        analytics.total_requests += 1
        analytics.last_request_date = timezone.now()
        
        if instance.status == 'approved' or instance.status == 'released':
            analytics.approved_requests += 1
        elif instance.status == 'rejected':
            analytics.rejected_requests += 1
        
        analytics.save()
        
        # Create activity log
        UserActivityLog.objects.create(
            user=instance.user,
            activity_type='request',
            supply=instance.supply,
            quantity=instance.quantity_requested,
            description=instance.purpose[:100]
        )
        
        # Update most requested items
        most_requested, _ = MostRequestedItem.objects.get_or_create(supply=instance.supply)
        most_requested.request_count += 1
        most_requested.last_requested = timezone.now()
        most_requested.save()
    
    else:  # Updated request
        # Update analytics if status changed to approved/rejected
        if instance.status in ['approved', 'released']:
            analytics, _ = RequestorBorrowerAnalytics.objects.get_or_create(user=instance.user)
            # Check if we already counted this as approved
            if instance.approved_at and (timezone.now() - instance.approved_at).total_seconds() < 60:
                # This was just approved/released
                if not hasattr(instance, '_approval_tracked'):
                    analytics.approved_requests += 1
                    analytics.save()
                    instance._approval_tracked = True


@receiver(post_save, sender=BorrowedItem)
def track_borrow_activity(sender, instance, created, **kwargs):
    """Track borrow/return activity"""
    if created:
        # Update analytics
        analytics, _ = RequestorBorrowerAnalytics.objects.get_or_create(user=instance.borrower)
        analytics.total_borrowings += 1
        analytics.last_borrow_date = timezone.now()
        analytics.save()
        
        # Create activity log
        UserActivityLog.objects.create(
            user=instance.borrower,
            activity_type='borrow',
            supply=instance.supply,
            quantity=instance.borrowed_quantity,
            description=f'Borrowed until {instance.return_deadline}'
        )
        
        # Update most requested items
        most_requested, _ = MostRequestedItem.objects.get_or_create(supply=instance.supply)
        most_requested.borrow_count += 1
        most_requested.last_borrowed = timezone.now()
        most_requested.save()
    
    else:  # Updated borrow item (e.g., returned)
        if instance.returned_at and not hasattr(instance, '_return_tracked'):
            # Item was just returned
            analytics, _ = RequestorBorrowerAnalytics.objects.get_or_create(user=instance.borrower)
            analytics.returned_items += 1
            
            # Track lost/damaged status
            if instance.return_status == 'lost':
                analytics.lost_items += 1
            elif instance.return_status == 'damaged':
                analytics.damaged_items += 1
            
            # Check for overdue
            if instance.is_overdue:
                analytics.overdue_items = max(0, analytics.overdue_items - 1)
            
            analytics.save()
            
            # Create activity log
            UserActivityLog.objects.create(
                user=instance.borrower,
                activity_type='return',
                supply=instance.supply,
                quantity=instance.borrowed_quantity,
                description=f'Returned item (was borrowed for {instance.duration_display})'
            )
            
            instance._return_tracked = True
