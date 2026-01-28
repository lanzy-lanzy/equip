# Generated migration for analytics models

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0008_supply_is_consumable'),
    ]

    operations = [
        migrations.CreateModel(
            name='RequestorBorrowerAnalytics',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_requests', models.PositiveIntegerField(default=0)),
                ('total_borrowings', models.PositiveIntegerField(default=0)),
                ('approved_requests', models.PositiveIntegerField(default=0)),
                ('rejected_requests', models.PositiveIntegerField(default=0)),
                ('returned_items', models.PositiveIntegerField(default=0)),
                ('overdue_items', models.PositiveIntegerField(default=0)),
                ('last_request_date', models.DateTimeField(blank=True, null=True)),
                ('last_borrow_date', models.DateTimeField(blank=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='analytics', to='inventory.user')),
            ],
            options={
                'verbose_name_plural': 'Requestor/Borrower Analytics',
            },
        ),
        migrations.CreateModel(
            name='UserActivityLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('activity_type', models.CharField(choices=[('request', 'Supply Request'), ('borrow', 'Borrow Item'), ('return', 'Return Item'), ('approval', 'Request Approval'), ('rejection', 'Request Rejection')], max_length=20)),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('description', models.TextField(blank=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('supply', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='inventory.supply')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='activity_logs', to='inventory.user')),
            ],
            options={
                'ordering': ['-timestamp'],
            },
        ),
        migrations.CreateModel(
            name='MostRequestedItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('request_count', models.PositiveIntegerField(default=0)),
                ('borrow_count', models.PositiveIntegerField(default=0)),
                ('last_requested', models.DateTimeField(blank=True, null=True)),
                ('last_borrowed', models.DateTimeField(blank=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('supply', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='request_stats', to='inventory.supply')),
            ],
            options={
                'ordering': ['-request_count', '-borrow_count'],
            },
        ),
        migrations.AddIndex(
            model_name='useractivitylog',
            index=models.Index(fields=['user', 'timestamp'], name='inventory_u_user_id_timestamp_idx'),
        ),
        migrations.AddIndex(
            model_name='useractivitylog',
            index=models.Index(fields=['activity_type', 'timestamp'], name='inventory_u_activity_timestamp_idx'),
        ),
    ]
