# Generated migration for borrowing duration feature

from django.db import migrations, models
from django.utils import timezone
from datetime import timedelta


def set_default_borrowed_date(apps, schema_editor):
    """Set borrowed_date to borrowed_at date for existing records"""
    BorrowedItem = apps.get_model('inventory', 'BorrowedItem')
    for item in BorrowedItem.objects.all():
        if not item.borrowed_date:
            item.borrowed_date = item.borrowed_at.date()
            item.save()


def set_default_return_deadline(apps, schema_editor):
    """Set return_deadline based on borrowed_date for existing records"""
    BorrowedItem = apps.get_model('inventory', 'BorrowedItem')
    for item in BorrowedItem.objects.all():
        if item.borrowed_date and not item.return_deadline:
            item.return_deadline = item.borrowed_date + timedelta(days=3)
            item.save()


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0006_notification'),
    ]

    operations = [
        migrations.AddField(
            model_name='borroweditem',
            name='borrowed_date',
            field=models.DateField(default=timezone.now, help_text='Date when the item was borrowed'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='borroweditem',
            name='borrow_duration_days',
            field=models.PositiveIntegerField(default=3, help_text='Number of days the item can be borrowed'),
        ),
        migrations.RunPython(set_default_borrowed_date),
        migrations.AlterField(
            model_name='borroweditem',
            name='return_deadline',
            field=models.DateField(blank=True, help_text='Date when the item must be returned (3 days from borrowed date)', null=True),
        ),
        migrations.RunPython(set_default_return_deadline),
    ]
