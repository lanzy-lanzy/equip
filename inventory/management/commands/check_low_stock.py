from django.core.management.base import BaseCommand
from django.contrib import messages
from django.db.models import F
from inventory.models import Supply, User
from inventory.utils import get_low_stock_items

class Command(BaseCommand):
    help = 'Check for low stock items and send alerts'

    def add_arguments(self, parser):
        parser.add_argument(
            '--notify-admins',
            action='store_true',
            help='Send notifications to admin users',
        )
        parser.add_argument(
            '--notify-gso',
            action='store_true',
            help='Send notifications to GSO staff',
        )

    def handle(self, *args, **options):
        # Get all low stock items
        low_stock_items = get_low_stock_items()
        
        if low_stock_items.exists():
            self.stdout.write(
                self.style.WARNING(
                    f'Found {low_stock_items.count()} low stock items:'
                )
            )
            
            for item in low_stock_items:
                message = f"ALERT: {item.name} is at low stock level ({item.quantity}/{item.min_stock_level}). Please consider restocking."
                self.stdout.write(f"  - {message}")
                
                # If notification options are enabled, we would send notifications here
                # This is a simplified version - in a real application, you might:
                # 1. Send email notifications
                # 2. Create in-app notifications
                # 3. Send SMS alerts
                # 4. Log to a monitoring system
                
                if options['notify_admins'] or options['notify_gso']:
                    # Get users to notify
                    users_to_notify = User.objects.none()
                    
                    if options['notify_admins']:
                        admins = User.objects.filter(role='admin')
                        users_to_notify = users_to_notify.union(admins)
                    
                    if options['notify_gso']:
                        gso_staff = User.objects.filter(role='gso_staff')
                        users_to_notify = users_to_notify.union(gso_staff)
                    
                    # In a real implementation, send notifications to these users
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"Would notify {users_to_notify.count()} users about {item.name}"
                        )
                    )
        else:
            self.stdout.write(
                self.style.SUCCESS('No low stock items found.')
            )