from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import F
from .models import BorrowedItem, Supply, Notification, User

def check_low_stock_alerts(supply, previous_quantity, new_quantity):
    """
    Check if a supply item is below its minimum stock level and return an alert message.
    Triggered when stock reaches or stays below minimum level after a decrease.
    """
    if new_quantity <= supply.min_stock_level and new_quantity < previous_quantity:
        msg = f"Alert: {supply.name} is low on stock ({new_quantity} remaining)."
        
        # Notify all admins and GSO staff
        recipients = User.objects.filter(role__in=['admin', 'gso_staff'])
        
        # Avoid spamming duplicate unread notifications for the same supply item
        title = f"Low Stock Alert: {supply.name}"
        
        for recipient in recipients:
            # Check if an unread notification for this supply already exists for this user
            exists = Notification.objects.filter(
                recipient=recipient,
                title=title,
                is_read=False
            ).exists()
            
            if not exists:
                Notification.objects.create(
                    recipient=recipient,
                    title=title,
                    message=msg,
                    url=f"/supplies/{supply.id}/",
                    level='warning'
                )
            
        return msg
    return None

def check_overdue_borrowed_items():
    """
    Check for borrowed items that are overdue or due soon and send alerts
    """
    # Get items that are not returned and have a deadline
    borrowed_items = BorrowedItem.objects.filter(
        returned_at__isnull=True,
        return_deadline__isnull=False
    ).select_related('borrower', 'supply')
    
    today = timezone.now().date()
    alerts_sent = 0
    
    for item in borrowed_items:
        # Check if item is overdue
        if item.is_overdue:
            # Send overdue alert
            send_overdue_alert(item)
            # Create an in-app notification for the borrower
            try:
                Notification.objects.create(
                    recipient=item.borrower,
                    title=f"Overdue item: {item.supply.name}",
                    message=(f"Your borrowed item '{item.supply.name}' (qty: {item.borrowed_quantity}) "
                             f"was due on {item.return_deadline.strftime('%b %d, %Y %H:%M')} and is now overdue."),
                    url='',
                    level='warning'
                )
            except Exception as e:
                print(f"Error creating notification: {e}")
            alerts_sent += 1
        else:
            # Check if item is due within 1 day
            if item.days_until_due is not None and item.days_until_due <= 1:
                # Send due soon alert
                send_due_soon_alert(item)
                # Create an in-app notification for due-soon
                try:
                    Notification.objects.create(
                        recipient=item.borrower,
                        title=f"Due soon: {item.supply.name}",
                        message=(f"Your borrowed item '{item.supply.name}' (qty: {item.borrowed_quantity}) "
                                 f"is due on {item.return_deadline.strftime('%b %d, %Y %H:%M')} ({abs(item.days_until_due)} day(s))."),
                        url='',
                        level='info'
                    )
                except Exception as e:
                    print(f"Error creating notification: {e}")
                alerts_sent += 1
    
    return alerts_sent

def send_overdue_alert(item):
    """
    Send an alert to the borrower that an item is overdue
    """
    try:
        subject = f"Overdue Item: {item.supply.name}"
        message = f"""
        Dear {item.borrower.get_full_name() or item.borrower.username},
        
        The item "{item.supply.name}" (Quantity: {item.borrowed_quantity}) 
        was due to be returned on {item.return_deadline.strftime('%B %d, %Y')}.
        
        Please return this item as soon as possible to avoid further restrictions 
        on your borrowing privileges.
        
        If you have already returned this item, please contact the GSO staff 
        to update the records.
        
        Thank you,
        GSO Team
        """
        
        # In a real implementation, you would send an email
        # For now, we'll just print to console
        print(f"OVERDUE ALERT: {subject}")
        print(message)
        
        # send_mail(
        #     subject,
        #     message,
        #     settings.DEFAULT_FROM_EMAIL,
        #     [item.borrower.email],
        #     fail_silently=False,
        # )
        
    except Exception as e:
        print(f"Error sending overdue alert: {e}")

def send_due_soon_alert(item):
    """
    Send an alert to the borrower that an item is due soon
    """
    try:
        subject = f"Due Soon: {item.supply.name}"
        message = f"""
        Dear {item.borrower.get_full_name() or item.borrower.username},
        
        The item "{item.supply.name}" (Quantity: {item.borrowed_quantity}) 
        is due to be returned on {item.return_deadline.strftime('%B %d, %Y')}.
        
        Please remember to return this item by the due date to avoid 
        restrictions on your borrowing privileges.
        
        Thank you,
        GSO Team
        """
        
        # In a real implementation, you would send an email
        # For now, we'll just print to console
        print(f"DUE SOON ALERT: {subject}")
        print(message)
        
        # send_mail(
        #     subject,
        #     message,
        #     settings.DEFAULT_FROM_EMAIL,
        #     [item.borrower.email],
        #     fail_silently=False,
        # )
        
    except Exception as e:
        print(f"Error sending due soon alert: {e}")

def has_overdue_items(user):
    """
    Check if a user has any overdue borrowed items
    """
    return BorrowedItem.objects.filter(
        borrower=user,
        returned_at__isnull=True,
        return_deadline__isnull=False,
        return_deadline__lt=timezone.now()
    ).exists()

def get_user_overdue_items(user):
    """
    Get all overdue items for a user
    """
    return BorrowedItem.objects.filter(
        borrower=user,
        returned_at__isnull=True,
        return_deadline__isnull=False,
        return_deadline__lt=timezone.now()
    ).select_related('supply')


def ensure_overdue_notifications():
    """
    Create in-app overdue notifications for admin/GSO users for borrowed items
    that are past their return deadline. This is idempotent
    and will not create duplicate unread notifications for the same borrow instance.
    """
    overdue_items = BorrowedItem.objects.filter(
        returned_at__isnull=True,
        return_deadline__isnull=False,
        return_deadline__lt=timezone.now().date()
    ).select_related('borrower', 'supply')
    
    recipients = User.objects.filter(role__in=['admin', 'gso_staff'])

    for item in overdue_items:
        title = f"Overdue Item: {item.supply.name}"
        msg = f"Item '{item.supply.name}' borrowed by {item.borrower.username} is overdue (Due: {item.return_deadline})."
        
        for recipient in recipients:
            # Check if THIS recipient already has an unread notification for this specific overdue item
            # We use the message to distinguish different overdue items
            exists_unread = Notification.objects.filter(
                recipient=recipient, 
                title=title,
                message=msg,
                is_read=False
            ).exists()
            
            if not exists_unread:
                try:
                    Notification.objects.create(
                        recipient=recipient,
                        title=title,
                        message=msg,
                        url=f"/borrowed-items/?status=overdue",
                        level='error'
                    )
                except Exception:
                    continue
    return True


def ensure_low_stock_notifications():
    """
    Create in-app low-stock notifications for admin/GSO users for supplies
    that are currently at or below their minimum stock level. This is idempotent
    and will not create duplicate unread notifications for the same supply.
    """
    low_supplies = Supply.objects.filter(quantity__lte=F('min_stock_level'))
    recipients = User.objects.filter(role__in=['admin', 'gso_staff'])

    for supply in low_supplies:
        title = f"Low Stock Alert: {supply.name}"
        msg = f"Alert: {supply.name} is low on stock ({supply.quantity} remaining)."
        
        for recipient in recipients:
            # Check if THIS recipient already has an unread notification for this supply
            exists_unread = Notification.objects.filter(
                recipient=recipient, 
                title=title, 
                is_read=False
            ).exists()
            
            if not exists_unread:
                try:
                    Notification.objects.create(
                        recipient=recipient,
                        title=title,
                        message=msg,
                        url=f"/supplies/{supply.id}/",
                        level='warning'
                    )
                except Exception:
                    continue
    return True
