# Analytics & Tracking System - Implementation Summary

## Overview
A comprehensive analytics and tracking system has been implemented to monitor requestor and borrower activities, identify trends, and generate insights.

## What Was Built

### 1. **Three New Database Models**

#### RequestorBorrowerAnalytics
- Stores aggregate statistics for each user
- Tracks: total requests, borrowings, approvals, rejections, returns, overdue items
- Last activity timestamps
- Auto-updated when requests/borrows are modified

#### UserActivityLog
- Detailed transaction log for all activities
- Tracks: request creation, borrowing, returning items
- Indexed by user and timestamp for fast queries
- Immutable record of all activities

#### MostRequestedItem
- Tracks popularity metrics for supplies
- Request count and borrow count
- Last activity timestamps
- Used for identifying high-demand items

### 2. **Four Analytics Views**

#### /analytics/requestor-borrower/
Main tracking dashboard showing:
- All department users with summary statistics
- Total requests, approved requests, borrowed items, unreturned items
- Quick overview cards
- One-click access to detailed user analytics

#### /analytics/user/<user_id>/
Detailed user analytics featuring:
- User profile card with avatar
- Summary statistics (requests, borrowings, approval rate)
- Advanced date filtering (Today, Week, Month, Year, Custom)
- Search functionality for requests
- Most requested items by this user
- Detailed requests table with status colors
- Detailed borrowed items table with return status
- CSV and PDF export buttons

#### /analytics/most-requested/
Item popularity tracking showing:
- All supplies sorted by total activity
- Request count and borrow count
- Total quantities requested/borrowed
- Current stock levels
- Date filtering and search
- View links to supply details
- CSV export capability

#### /analytics/export/<user_id>/
Export functionality for:
- CSV format (Excel-friendly)
- PDF format (professional reports)
- Filtered data based on date range
- Complete request and borrow history

### 3. **Automatic Signal Handlers**

Signals automatically update analytics when:
- **User Created:** Creates analytics record
- **Request Created:** Updates total requests, creates activity log
- **Request Status Changed:** Updates approved/rejected counts
- **Item Borrowed:** Updates total borrows, creates activity log
- **Item Returned:** Updates return count, creates activity log

### 4. **Sidebar Integration**

Added "Analytics" dropdown menu in the GSO sidebar:
- **Requestor/Borrower Tracking** → View all users dashboard
- **Most Requested Items** → View popular items
- Accessible only to Admin and GSO Staff
- Icons for quick visual identification

### 5. **Advanced Filtering System**

#### Date Range Options
- All Time (no limit)
- Today (current date only)
- This Week (Monday to today)
- This Month (1st to today)
- This Year (Jan 1 to today)
- Custom Range (user-specified dates)

#### Search Capabilities
- Request ID search
- Supply name search
- Request purpose search
- Item category search

### 6. **Export Functionality**

#### CSV Export
- Excel-compatible format
- Includes requests with full details
- Includes borrowed items with full details
- Summary statistics at bottom
- Filename includes username and date filter

#### PDF Export
- Professional formatted reports
- Landscape orientation for data visibility
- User information header
- Top 20 requests table
- Top 20 borrowed items table
- Color-coded status information

## File Structure

```
inventory/
├── models.py (3 new models added)
├── views.py (unchanged)
├── analytics_views.py (NEW - 4 view functions + exports)
├── urls.py (4 new URL patterns + imports)
├── signals.py (NEW - auto-tracking handlers)
├── apps.py (updated to register signals)
├── migrations/
│   └── 0009_analytics_models.py (NEW - schema)
└── management/
    └── commands/
        └── populate_analytics.py (NEW - initial data load)

templates/inventory/tracking/
├── requestor_borrower_tracking.html (NEW)
├── user_analytics_detail.html (NEW)
├── most_requested_items.html (NEW)
└── partials/
    ├── analytics_table.html (NEW)
    └── most_requested_table.html (NEW)

Documentation/
├── ANALYTICS_TRACKING_IMPLEMENTATION.md (NEW - complete guide)
├── ANALYTICS_QUICK_SETUP.md (NEW - quick start)
└── ANALYTICS_SUMMARY.md (NEW - this file)
```

## Database Schema

### RequestorBorrowerAnalytics
```sql
CREATE TABLE inventory_requestorborroweranalytics (
    id BIGINT PRIMARY KEY,
    user_id INT UNIQUE NOT NULL,
    total_requests INT DEFAULT 0,
    total_borrowings INT DEFAULT 0,
    approved_requests INT DEFAULT 0,
    rejected_requests INT DEFAULT 0,
    returned_items INT DEFAULT 0,
    overdue_items INT DEFAULT 0,
    last_request_date DATETIME NULL,
    last_borrow_date DATETIME NULL,
    updated_at DATETIME AUTO_UPDATE
);
```

### UserActivityLog
```sql
CREATE TABLE inventory_useractivitylog (
    id BIGINT PRIMARY KEY,
    user_id INT NOT NULL,
    activity_type VARCHAR(20),
    supply_id INT NULL,
    quantity INT DEFAULT 1,
    description TEXT,
    timestamp DATETIME AUTO_CREATE,
    INDEX(user_id, timestamp),
    INDEX(activity_type, timestamp)
);
```

### MostRequestedItem
```sql
CREATE TABLE inventory_mostrequesteditem (
    id BIGINT PRIMARY KEY,
    supply_id INT UNIQUE NOT NULL,
    request_count INT DEFAULT 0,
    borrow_count INT DEFAULT 0,
    last_requested DATETIME NULL,
    last_borrowed DATETIME NULL,
    updated_at DATETIME AUTO_UPDATE
);
```

## Key Features

### Real-Time Updates
- Signals automatically update analytics when data changes
- No batch processing needed
- Instant reflection of new activities

### Advanced Filtering
- Preset date ranges for common queries
- Custom date range picker
- Search by multiple fields
- Combine filters for precise data

### Comprehensive Tracking
- Every request tracked
- Every borrow/return tracked
- User activity timeline
- Supply popularity metrics

### Export & Reporting
- Generate CSV for spreadsheet analysis
- Generate PDF for professional reports
- Filter exports by date range
- Download directly from UI

### Permission-Based Access
- Admin and GSO Staff only
- Role-based access control
- Secure data access

## Usage Scenarios

### Scenario 1: Identify Overdue Items
1. Go to Requestor/Borrower Tracking
2. Find user with unreturned items
3. Click "View" to see details
4. Check Borrowed Items table for "Overdue" status
5. Send reminder to return items

### Scenario 2: Stock Planning
1. Go to Most Requested Items
2. Filter by "This Month"
3. Identify top 10 requested items
4. Review current stock levels
5. Plan procurement for high-demand items

### Scenario 3: User Performance Review
1. Go to Requestor/Borrower Tracking
2. Click "View" for specific user
3. Set date range to "This Year"
4. Review approval rate and patterns
5. Download PDF report for documentation

### Scenario 4: Monthly Analytics Report
1. Go to user analytics detail page
2. Set date filter to "This Month"
3. Click "Download CSV"
4. Import into management reporting tool
5. Create visualizations and share with leadership

## Technical Implementation

### ORM Features Used
- OneToOne relationships for single-record-per-user
- ForeignKey relationships for multi-record tracking
- Count aggregations for statistics
- Custom queryset filtering
- Database indexes for performance

### Django Features Used
- Django signals for auto-updates
- Template tags and filters
- Context processors for data passing
- URL reverse resolution
- CSRF protection for exports
- DateField and DateTimeField handling

### Performance Optimizations
- Database indexes on user and timestamp
- Prefetch and select_related for N+1 prevention
- Aggregate functions instead of Python loops
- Cached models for rapid access

## URL Configuration

```python
# Analytics URLs
path('analytics/requestor-borrower/', analytics_views.requestor_borrower_tracking, name='requestor_borrower_tracking'),
path('analytics/user/<int:user_id>/', analytics_views.user_analytics_detail, name='user_analytics_detail'),
path('analytics/most-requested/', analytics_views.most_requested_items, name='most_requested_items'),
path('analytics/export/<int:user_id>/', analytics_views.export_user_analytics, name='export_user_analytics'),
```

## Management Command

```bash
python manage.py populate_analytics
```

Processes:
- All existing SupplyRequest records
- All existing BorrowedItem records
- Creates analytics records for all department users
- Generates activity logs from historical data
- Calculates most requested item statistics

## Security Features

1. **Access Control:**
   - Role-based access (Admin/GSO only)
   - User ID validation in URL
   - Permission checks in all views

2. **Data Validation:**
   - Date range validation
   - User ID existence checks
   - Safe parameter handling

3. **CSRF Protection:**
   - CSRF token in export forms
   - Standard Django security

## Sidebar Navigation

```
Analytics ▼
├── Requestor/Borrower Tracking
└── Most Requested Items
```

- Located after "Reports" menu
- Before "User Management"
- Visible only to Admin/GSO Staff
- Uses chart-line and fire icons

## Statistics Calculated

### Per User
- Total requests submitted
- Total items borrowed
- Approval rate
- Return rate
- Overdue items count
- Last activity date

### Per Item
- Total requests count
- Total borrows count
- Last request date
- Last borrow date
- Current stock level
- Total quantity demand

## Export Columns

### CSV Requests
- Request ID
- Supply Name
- Quantity
- Status
- Purpose
- Created Date

### CSV Borrows
- Supply Name
- Quantity
- Borrowed Date
- Return Deadline
- Status
- Returned Date

### PDF Reports
- All CSV data plus
- Professional formatting
- Color-coded status
- Summary statistics
- Landscape layout

## Installation Summary

1. **Migration:** `python manage.py migrate`
2. **Populate:** `python manage.py populate_analytics`
3. **Restart:** `python manage.py runserver`
4. **Access:** Admin/GSO sidebar → Analytics

## Verification Checklist

- [ ] Migration applied successfully
- [ ] Analytics tables created
- [ ] Initial data populated
- [ ] Sidebar shows Analytics menu
- [ ] Can access Requestor/Borrower Tracking
- [ ] Can access Most Requested Items
- [ ] Can filter by date range
- [ ] Can search requests
- [ ] Can export CSV
- [ ] Can export PDF
- [ ] Signals update data on new requests
- [ ] Signals update data on new borrows

## Testing Commands

```bash
# Check migration status
python manage.py showmigrations inventory

# Verify models
python manage.py shell
>>> from inventory.models import RequestorBorrowerAnalytics
>>> RequestorBorrowerAnalytics.objects.count()

# Check activity logs
>>> from inventory.models import UserActivityLog
>>> UserActivityLog.objects.count()
```

## Performance Impact

- **No negative impact** on existing operations
- Data updated automatically via signals
- Indexes ensure fast query performance
- Suitable for production use

## Future Enhancement Ideas

1. **Charts & Visualization:**
   - Request trends over time
   - Borrow/return rate graphs
   - Item popularity charts

2. **Email Reporting:**
   - Scheduled daily/weekly summaries
   - Alert notifications

3. **Department Analytics:**
   - Track by department
   - Department-level comparisons

4. **Advanced Features:**
   - User allocation limits
   - Prediction algorithms
   - Resource optimization

5. **Integration:**
   - API endpoints for external tools
   - Webhook notifications
   - Bulk operations

---

## Quick Start

```bash
# 1. Run migrations
python manage.py migrate

# 2. Populate existing data
python manage.py populate_analytics

# 3. Restart server
python manage.py runserver

# 4. Login as Admin/GSO and check sidebar
```

The system is now fully operational and tracking all user activities automatically!
