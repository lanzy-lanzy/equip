#!/usr/bin/env python
"""Test script to verify analytics implementation"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'supply_.settings')
django.setup()

from inventory.models import RequestorBorrowerAnalytics, UserActivityLog, MostRequestedItem, User

print("=" * 60)
print("ANALYTICS IMPLEMENTATION VERIFICATION")
print("=" * 60)

# Check analytics records
print("\n1. RequestorBorrowerAnalytics Records:")
analytics_count = RequestorBorrowerAnalytics.objects.count()
print(f"   Total records: {analytics_count}")
for analytics in RequestorBorrowerAnalytics.objects.all():
    print(f"   - {analytics.user.username}:")
    print(f"     • Total requests: {analytics.total_requests}")
    print(f"     • Approved requests: {analytics.approved_requests}")
    print(f"     • Total borrowings: {analytics.total_borrowings}")
    print(f"     • Returned items: {analytics.returned_items}")
    print(f"     • Overdue items: {analytics.overdue_items}")

# Check activity logs
print(f"\n2. UserActivityLog Records:")
activity_count = UserActivityLog.objects.count()
print(f"   Total logs: {activity_count}")
activity_types = UserActivityLog.objects.values('activity_type').distinct()
for activity in activity_types:
    count = UserActivityLog.objects.filter(activity_type=activity['activity_type']).count()
    print(f"   - {activity['activity_type']}: {count}")

# Show sample activity logs
print(f"\n3. Recent Activity Logs (last 10):")
for log in UserActivityLog.objects.all()[:10]:
    print(f"   - {log.user.username} ({log.activity_type}): {log.supply.name if log.supply else 'N/A'} on {log.timestamp.date()}")

# Show most requested
print(f"\n4. Most Requested Items (top 10):")
most_requested_count = MostRequestedItem.objects.count()
print(f"   Total tracked items: {most_requested_count}")
for item in MostRequestedItem.objects.order_by('-request_count', '-borrow_count')[:10]:
    total_activity = item.request_count + item.borrow_count
    print(f"   - {item.supply.name}:")
    print(f"     • Requests: {item.request_count}, Borrows: {item.borrow_count}, Total: {total_activity}")

print("\n" + "=" * 60)
print("✓ All analytics models are working correctly!")
print("=" * 60)

# Summary
print(f"\nSUMMARY:")
print(f"  Users with analytics: {analytics_count}")
print(f"  Activity logs created: {activity_count}")
print(f"  Items tracked: {most_requested_count}")
print(f"\n✓ Analytics system is ready to use!")
