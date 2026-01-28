# Analytics & Tracking - Quick Setup Guide

## What Was Added

A complete analytics and tracking system for monitoring requestors and borrowers with:
- Real-time statistics tracking
- Customizable date range filtering
- Advanced search functionality
- CSV and PDF export capabilities
- Most requested items analytics
- User activity logging

## Step-by-Step Setup

### 1. Database Migration
```bash
python manage.py migrate
```

This creates three new tables:
- `inventory_requestorborroweranalytics` - Aggregate user statistics
- `inventory_useractivitylog` - Detailed activity logs
- `inventory_mostrequesteditem` - Item popularity metrics

### 2. Populate Existing Data
```bash
python manage.py populate_analytics
```

This analyzes all existing requests and borrows, creating:
- Analytics records for each department user
- Activity logs from historical data
- Most requested item statistics

### 3. Verify Setup
1. Log in as Admin or GSO Staff
2. Check sidebar - you should see "Analytics" menu section
3. Click "Requestor/Borrower Tracking" to view dashboard

## Files Added

### Views (`inventory/analytics_views.py`)
- `requestor_borrower_tracking()` - Main tracking dashboard
- `user_analytics_detail()` - User-specific analytics with filters
- `most_requested_items()` - Most popular items across all users
- `export_user_analytics()` - CSV/PDF export functionality

### Models (in `inventory/models.py`)
- `RequestorBorrowerAnalytics` - User statistics
- `UserActivityLog` - Activity tracking
- `MostRequestedItem` - Item popularity

### Signals (`inventory/signals.py`)
Automatically updates analytics when:
- New supply requests are created/updated
- Items are borrowed/returned
- New users are registered

### Templates
- `templates/inventory/tracking/requestor_borrower_tracking.html` - Dashboard
- `templates/inventory/tracking/user_analytics_detail.html` - User analytics
- `templates/inventory/tracking/most_requested_items.html` - Item popularity
- `templates/inventory/tracking/partials/*.html` - HTMX partials

### URLs (updated `inventory/urls.py`)
```python
path('analytics/requestor-borrower/', ...)
path('analytics/user/<int:user_id>/', ...)
path('analytics/most-requested/', ...)
path('analytics/export/<int:user_id>/', ...)
```

### Sidebar (updated `templates/base.html`)
Added "Analytics" dropdown with two menu items:
- Requestor/Borrower Tracking
- Most Requested Items

## Main Features Overview

### 1. **Tracking Dashboard**
- View all department users
- See request/borrow statistics at a glance
- Click "View" to see detailed analytics for any user

### 2. **User Analytics Detail**
Features:
- **Summary Cards:** Total requests, borrowed items, unreturned items, approval rate
- **Filters:**
  - Date range (Today, This Week, This Month, This Year, Custom)
  - Search requests by ID, supply name, or purpose
- **Tables:**
  - Supply Requests (with status colors)
  - Borrowed Items (with return status)
  - Most Requested Items by this user
- **Export:**
  - Download as CSV
  - Download as PDF

### 3. **Most Requested Items**
Shows:
- All supplies sorted by popularity
- Request count vs borrow count
- Total quantities
- Current stock levels
- Filterable by date range and search
- Exportable to CSV

## Usage Examples

### Finding User with Most Requests
1. Go to Analytics → Requestor/Borrower Tracking
2. Sort users by "Total Requests" column
3. Click "View" on the user

### Analyzing Weekly Trends
1. Go to Analytics → User Detail (for specific user)
2. Set date filter to "This Week"
3. Apply filters to see only this week's activity
4. Download CSV for further analysis

### Identifying Stock Issues
1. Go to Analytics → Most Requested Items
2. Look for high request count with low current stock
3. Click item to view supply details
4. Consider increasing stock levels for popular items

### Tracking Overdue Items
1. Go to Analytics → User Detail (for specific user)
2. Check "Borrowed Items" table
3. Items marked "Overdue" in red need follow-up
4. Summary card shows total overdue count

## Key Data Points Tracked

### Per User:
- Total requests submitted
- Approved request count
- Rejected request count
- Total items borrowed
- Items successfully returned
- Overdue items count
- Last request date
- Last borrow date

### Per Supply:
- Total request count
- Total borrow count
- Last request date
- Last borrow date

### Activity Logs Include:
- User who performed action
- Type of action (request, borrow, return, etc.)
- Supply involved
- Quantity
- Timestamp
- Description/notes

## Filter Guide

### Date Range Options
- **All Time:** No filtering by date
- **Today:** Only today's activities
- **This Week:** Monday through today
- **This Month:** 1st of month through today
- **This Year:** January 1st through today
- **Custom:** User-specified start and end dates

### Search Fields
- **In User Analytics:**
  - Request ID: REQ-YYYYMMDD-XXXX format
  - Supply name: Partial matching
  - Request purpose: Keyword search

- **In Most Requested:**
  - Item name: Partial matching
  - Category: Exact matching

## Export Formats

### CSV Export
Perfect for:
- Analysis in Excel/Google Sheets
- Data import to other systems
- Archival and record-keeping

Includes:
- Request headers: Request ID, Supply, Quantity, Status, Purpose, Date
- Borrow headers: Supply, Quantity, Borrowed Date, Return Deadline, Status, Returned Date
- Summary statistics

### PDF Export
Perfect for:
- Professional reports
- Printing
- Email distribution
- Executive summaries

Includes:
- User information header
- Top 20 requests table
- Top 20 borrowed items table
- Landscape orientation for readability

## Sidebar Navigation

In the left sidebar:
1. Find "Analytics" section (after Reports)
2. Two submenu items appear:
   - **Requestor/Borrower Tracking** - See all users
   - **Most Requested Items** - See popular items

All analytics pages are restricted to Admin and GSO Staff users.

## Permission Requirements

Only accessible to:
- Admin role
- GSO Staff role

Department Users cannot access analytics pages.

## Performance Notes

- Analytics data is updated in real-time via Django signals
- No background jobs required
- Queries are optimized with database indexes
- Suitable for 1000+ users and 10000+ transactions

## Troubleshooting

**Q: Analytics menu not showing**
A: Ensure you're logged in as Admin or GSO Staff

**Q: No data appears after setup**
A: Run `python manage.py populate_analytics` to process existing data

**Q: Export button shows error**
A: Ensure ReportLab is installed: `pip install reportlab`

**Q: Custom date range not working**
A: Check date format is YYYY-MM-DD and start date is before end date

## Next Steps

1. **Explore the Dashboard:**
   - Navigate to Analytics → Requestor/Borrower Tracking
   - Review statistics for each user
   - Click "View" on any user to see details

2. **Test Filtering:**
   - Try different date ranges
   - Use search to find specific requests
   - Export data in different formats

3. **Monitor Trends:**
   - Identify most-requested items
   - Track user request patterns
   - Monitor overdue items

4. **Use Reports:**
   - Generate CSV/PDF reports
   - Share with management
   - Track performance over time

---

For detailed information, see `ANALYTICS_TRACKING_IMPLEMENTATION.md`
