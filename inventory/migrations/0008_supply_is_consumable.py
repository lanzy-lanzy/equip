# Generated migration for is_consumable field

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0007_borrowing_duration_fields'),
    ]

    operations = [
        migrations.AddField(
            model_name='supply',
            name='is_consumable',
            field=models.BooleanField(default=False, help_text='Check if this item is consumable (e.g., paper, pens). Unchecked means non-consumable (e.g., equipment)'),
        ),
    ]
