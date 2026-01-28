# Analytics & Tracking System - Quick Reference

## Quick Access

| Feature | URL | Access |
|---------|-----|--------|
| Tracking Dashboard | `/analytics/requestor-borrower/` | Admin, GSO |
| User Analytics | `/analytics/user/<user_id>/` | Admin, GSO |
| Most Requested Items | `/analytics/most-requested/` | Admin, GSO |
| Export CSV | `/analytics/export/<user_id>/?format=csv` | Admin, GSO |
| Export PDF | `/analytics/export/<user_id>/?format=pdf` | Admin, GSO |

## Navigation Path

```
Sidebar → Analytics ▼
  ├── Requestor/Borrower Tracking
  └── Most Requested Items
```

## Key Metrics Tracked

### Per User
- Total requests submitted
- Approved requests count
- Rejected requests count  
- Items borrowed
- Items returned
- Overdue items
- Last activity date
- Approval rate

### Per Item
- Total request count
- Total borrow count
- Last requested date
- Last borrowed date

## Date Filter Options

| Filter | Period |
|--------|--------|
| All Time | No limit |
| Today | Current date only |
| This Week | Monday → Now |
| This Month | 1st → Now |
| This Year | Jan 1 → Now |
| Custom | User-selected range |

## Database Models

```
RequestorBorrowerAnalytics
├── user (OneToOne)
├── total_requests
├── total_borrowings
├── approved_requests
├── rejected_requests
├── returned_items
├── overdue_items
├── last_request_date
└── last_borrow_date

UserActivityLog
├── user (ForeignKey)
├── activity_type (request|borrow|return)
├── supply (ForeignKey)
├── quantity
├── description
└── timestamp

MostRequestedItem
├── supply (OneToOne)
├── request_count
├── borrow_count
├── last_requested
└── last_borrowed
```

## Management Commands

```bash
# Populate analytics from existing data
python manage.py populate_analytics
```

## Sidebar Menu Items

| Menu | Icon | URL |
|------|------|-----|
| Requestor/Borrower Tracking | fa-users | requestor_borrower_tracking |
| Most Requested Items | fa-fire | most_requested_items |

## Export Formats

### CSV
- Excel-compatible
- Contains requests & borrows
- Includes summary stats
- Filename: `analytics_<username>_<filter>.csv`

### PDF
- Professional format
- Landscape orientation
- Top 20 items per section
- Color-coded status

## File Locations

| File | Purpose |
|------|---------|
| `inventory/analytics_views.py` | View logic |
| `inventory/signals.py` | Auto-tracking |
| `inventory/models.py` | Data models |
| `inventory/urls.py` | URL routing |
| `templates/inventory/tracking/` | HTML templates |

## API Parameters

### Analytics Detail View
```
GET /analytics/user/<user_id>/
  ?date_filter=<filter>&start_date=YYYY-MM-DD&end_date=YYYY-MM-DD&search=<term>
```

### Most Requested View
```
GET /analytics/most-requested/
  ?date_filter=<filter>&start_date=YYYY-MM-DD&end_date=YYYY-MM-DD&search=<term>
```

### Export
```
GET /analytics/export/<user_id>/
  ?format=<csv|pdf>&date_filter=<filter>&start_date=<date>&end_date=<date>
```

## Templates

| Template | Purpose |
|----------|---------|
| `requestor_borrower_tracking.html` | User dashboard |
| `user_analytics_detail.html` | User detail page |
| `most_requested_items.html` | Items popularity |
| `partials/analytics_table.html` | HTMX partial |
| `partials/most_requested_table.html` | HTMX partial |

## Color Coding

| Color | Meaning |
|-------|---------|
| Blue | Request metrics |
| Green | Return/Success |
| Purple | Total activity |
| Orange | Warning/High |
| Red | Overdue/Error |
| Yellow | Pending/In Progress |

## Status Badges

### Request Status
- **Green:** Released (completed)
- **Blue:** Approved (pending release)
- **Yellow:** Pending (awaiting approval)
- **Red:** Rejected (denied)

### Borrow Status
- **Green:** Returned
- **Orange:** Active (due soon)
- **Red:** Overdue
- **Gray:** Cancelled

## Permission Requirements

### Can Access Analytics
- ✓ Admin users
- ✓ GSO Staff
- ✗ Department users

## Setup Commands

```bash
# 1. Apply database changes
python manage.py migrate

# 2. Populate existing data
python manage.py populate_analytics

# 3. Restart server
python manage.py runserver

# 4. Login and verify (Admin/GSO)
# Navigate to: Sidebar → Analytics
```

## Common Tasks

### View All Users' Analytics
1. Login as Admin/GSO
2. Click: Sidebar → Analytics → Requestor/Borrower Tracking
3. View user list with summary stats

### Check Specific User's Activity
1. From tracking dashboard
2. Find user in table
3. Click "View" button
4. See detailed analytics with all requests/borrows

### Find Most Popular Items
1. Click: Sidebar → Analytics → Most Requested Items
2. Items sorted by total activity
3. Filter by date or search
4. Check current stock vs. demand

### Export User Report
1. Go to user analytics page
2. Select date range
3. Click "Download CSV" or "Download PDF"
4. Save/share report

### Track Overdue Items
1. User analytics detail page
2. Scroll to "Borrowed Items" table
3. Look for items marked "Overdue"
4. Summary card shows total overdue

## Tips & Tricks

1. **Quick Analysis:** Use "This Month" filter for current month analysis
2. **Custom Reports:** Use custom date range for specific periods
3. **CSV Export:** Best for spreadsheet manipulation
4. **PDF Export:** Best for printing and sharing
5. **Search:** Use partial matches (e.g., "paper" finds all paper items)
6. **Trends:** Compare month-to-month data by exporting multiple periods

## Troubleshooting Quick Fix

| Issue | Solution |
|-------|----------|
| No Analytics menu | Verify user is Admin/GSO staff |
| No data showing | Run `populate_analytics` command |
| Export not working | Check ReportLab installed: `pip install reportlab` |
| Date filter not working | Verify date format YYYY-MM-DD |

## Performance Notes

- Optimized queries with indexes
- Real-time updates via signals
- Suitable for 1000+ users
- No background jobs needed

## Support Files

- `ANALYTICS_TRACKING_IMPLEMENTATION.md` - Full documentation
- `ANALYTICS_QUICK_SETUP.md` - Setup guide
- `ANALYTICS_SUMMARY.md` - Implementation summary
- `IMPLEMENTATION_CHECKLIST.md` - Completion checklist

---

**Version:** 1.0  
**Last Updated:** December 6, 2025  
**Status:** Production Ready
