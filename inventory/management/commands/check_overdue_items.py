from django.core.management.base import BaseCommand
from django.utils import timezone
from ...utils import check_overdue_borrowed_items

class Command(BaseCommand):
    help = 'Check for overdue borrowed items and send alerts'
    
    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('Checking for overdue borrowed items...')
        )
        
        alerts_sent = check_overdue_borrowed_items()
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully checked overdue items. Sent {alerts_sent} alerts.'
            )
        )