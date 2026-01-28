# Analytics & Tracking System Implementation

## Overview
A comprehensive tracking system for supply requests and borrowing activities. Allows GSO/Admin users to monitor requestor and borrower behavior patterns and identify trends.

## Features

### 1. **Requestor & Borrower Tracking Dashboard**
- **Location:** Sidebar → Analytics → Requestor/Borrower Tracking
- **URL:** `/analytics/requestor-borrower/`
- **Access:** Admin and GSO Staff only

**Features:**
- View all department users with summary statistics
- Quick glance metrics:
  - Total Users
  - Active Borrowers
  - Total Requests
  - Overdue Items
- User table showing:
  - Username and Department
  - Total Requests count
  - Approved Requests count
  - Items Borrowed count
  - Unreturned Items count
  - Last Activity timestamp
  - View analytics button for each user

### 2. **User Analytics Detail Page**
- **Location:** Click "View" button from tracking dashboard
- **URL:** `/analytics/user/<user_id>/`
- **Access:** Admin and GSO Staff only

**Features:**
- Detailed user profile with avatar
- Summary cards:
  - Total Requests
  - Items Borrowed
  - Unreturned Items
  - Approval Rate percentage
- Advanced Filtering:
  - Date Range: All Time, Today, This Week, This Month, This Year, Custom Range
  - Custom date picker for flexible filtering
  - Search functionality for requests
- Most Requested Items by user (top 5)
- Supply Requests table with:
  - Request ID
  - Supply name
  - Quantity
  - Status (with color coding)
  - Creation date
  - Link to request detail
- Borrowed Items table with:
  - Supply name
  - Quantity
  - Borrowed Date
  - Return Deadline
  - Status (Active/Overdue/Returned)
  - Link to manage item
- **Export Options:**
  - Download CSV
  - Download PDF

### 3. **Most Requested & Borrowed Items**
- **Location:** Sidebar → Analytics → Most Requested Items
- **URL:** `/analytics/most-requested/`
- **Access:** Admin and GSO Staff only

**Features:**
- Comprehensive item popularity tracking
- Filtering:
  - Date Range: All Time, Today, This Week, This Month, This Year, Custom Range
  - Search by item name or category
- Items table showing:
  - Item Name
  - Category
  - Current Stock quantity
  - Request Count (badge)
  - Total Quantity Requested
  - Borrow Count (badge)
  - Total Quantity Borrowed
  - Total Activity (sum of requests + borrows)
  - Link to supply detail page
- **Export Options:**
  - Download CSV
  - Client-side CSV export via JavaScript

### 4. **Activity Tracking**
The system automatically logs all user activities:
- Supply Requests creation
- Borrowing items
- Returning items
- Request Approvals
- Request Rejections

**Data Tracked:**
- User who performed the action
- Activity type
- Supply involved
- Quantity
- Timestamp
- Description

## Database Models

### RequestorBorrowerAnalytics
Stores aggregate statistics for each user:
```python
- user: OneToOne(User)
- total_requests: Count of all requests
- total_borrowings: Count of all borrows
- approved_requests: Count of approved requests
- rejected_requests: Count of rejected requests
- returned_items: Count of returned items
- overdue_items: Count of overdue items
- last_request_date: Timestamp of last request
- last_borrow_date: Timestamp of last borrow
- updated_at: Auto-updated timestamp
```

### UserActivityLog
Detailed log of all user activities:
```python
- user: ForeignKey(User)
- activity_type: Choice field (request, borrow, return, approval, rejection)
- supply: ForeignKey(Supply, nullable)
- quantity: Positive integer
- description: Text field
- timestamp: Auto-created datetime
```

### MostRequestedItem
Tracks popularity metrics for supplies:
```python
- supply: OneToOne(Supply)
- request_count: Total requests
- borrow_count: Total borrows
- last_requested: Timestamp of last request
- last_borrowed: Timestamp of last borrow
- updated_at: Auto-updated timestamp
```

## API Endpoints

### Analytics Endpoints
1. **GET /analytics/requestor-borrower/**
   - Main tracking dashboard
   - Returns: List of all department users with analytics

2. **GET /analytics/user/<user_id>/**
   - User-specific analytics
   - Query Parameters:
     - `date_filter`: all, today, week, month, year, custom
     - `start_date`: YYYY-MM-DD (for custom range)
     - `end_date`: YYYY-MM-DD (for custom range)
     - `search`: Search term for requests
   - Returns: Detailed user analytics with filtered data

3. **GET /analytics/most-requested/**
   - Most popular items
   - Query Parameters: Same as user analytics
   - Returns: Items sorted by total activity

4. **GET /analytics/export/<user_id>/**
   - Export user analytics
   - Query Parameters:
     - `format`: csv or pdf
     - All filter parameters from detail view
   - Returns: CSV or PDF file

## URL Configuration

All URLs are configured in `inventory/urls.py`:
```python
path('analytics/requestor-borrower/', analytics_views.requestor_borrower_tracking, name='requestor_borrower_tracking'),
path('analytics/user/<int:user_id>/', analytics_views.user_analytics_detail, name='user_analytics_detail'),
path('analytics/most-requested/', analytics_views.most_requested_items, name='most_requested_items'),
path('analytics/export/<int:user_id>/', analytics_views.export_user_analytics, name='export_user_analytics'),
```

## Sidebar Navigation

The Analytics section is added to the GSO sidebar:
- **Location:** After Reports, before User Management
- **Icon:** chart-line
- **Submenu Items:**
  1. Requestor/Borrower Tracking (users icon)
  2. Most Requested Items (fire icon)

## Automatic Signals

Django signals automatically update analytics when:
1. **User Created:** Creates new RequestorBorrowerAnalytics record
2. **SupplyRequest Created/Updated:**
   - Increments total_requests
   - Increments approved_requests if status changes to approved/released
   - Increments rejected_requests if rejected
   - Updates last_request_date
   - Creates UserActivityLog entry
   - Updates MostRequestedItem.request_count

3. **BorrowedItem Created/Updated:**
   - Increments total_borrowings on creation
   - Increments returned_items on return
   - Updates overdue_items count
   - Creates UserActivityLog entries
   - Updates MostRequestedItem.borrow_count

## Management Commands

### populate_analytics
Populates analytics for all existing data:
```bash
python manage.py populate_analytics
```

**What it does:**
- Creates RequestorBorrowerAnalytics records for all department users
- Calculates statistics from existing requests/borrows
- Creates MostRequestedItem records for all supplies
- Generates UserActivityLog entries from historical data

## Templates

### Main Templates
- `templates/inventory/tracking/requestor_borrower_tracking.html`
  - Tracking dashboard with user list

- `templates/inventory/tracking/user_analytics_detail.html`
  - Detailed user analytics with filters
  - Statistics cards
  - Requests and borrows tables
  - Export buttons

- `templates/inventory/tracking/most_requested_items.html`
  - Most popular items list
  - Activity metrics
  - Export options

### Partial Templates (HTMX)
- `templates/inventory/tracking/partials/analytics_table.html`
  - Requests table partial
  
- `templates/inventory/tracking/partials/most_requested_table.html`
  - Items table partial

## Export Functionality

### CSV Export
- Available from user analytics and most requested items pages
- Contains:
  - Requests with full details
  - Borrowed items with full details
  - Summary statistics
- Downloads as: `analytics_<username>_<date_filter>.csv`

### PDF Export
- Professional formatted PDF reports
- Includes:
  - User information
  - Request table (top 20 items)
  - Borrowed items table (top 20 items)
  - Landscape orientation for better data visibility
- Downloads as: `analytics_<username>_<date_filter>.pdf`

## Date Range Filtering

### Preset Filters
1. **All Time:** No date limit
2. **Today:** Current date only
3. **This Week:** Monday to current day
4. **This Month:** 1st of month to current day
5. **This Year:** January 1st to current day
6. **Custom Range:** User-specified start and end dates

### Custom Date Range
- Uses HTML5 date inputs
- Format: YYYY-MM-DD
- Validates date range on backend
- Falls back to 30 days if invalid dates provided

## Search Functionality

### Available in:
1. **User Analytics Detail:**
   - Search request ID
   - Search supply name
   - Search request purpose

2. **Most Requested Items:**
   - Search by item name
   - Search by category

## Styling & UI

- **Color Scheme:**
  - Blue badges: Request counts
  - Green badges: Borrow counts
  - Purple badges: Total activity
  - Red badges: Overdue items
  - Orange badges: Warning states

- **Icons:**
  - Analytics: `fas fa-chart-line`
  - Requestor/Borrower: `fas fa-users`
  - Most Requested: `fas fa-fire`
  - Export CSV: `fas fa-download`
  - Export PDF: `fas fa-file-pdf`

- **Responsive Design:**
  - Mobile-friendly tables
  - Responsive grid layouts
  - Touch-friendly buttons
  - Collapsible sections on mobile

## Performance Optimizations

1. **Database Indexing:**
   - `UserActivityLog` indexed on (user, timestamp)
   - `UserActivityLog` indexed on (activity_type, timestamp)

2. **Query Optimization:**
   - Uses `select_related()` for foreign keys
   - Uses `prefetch_related()` for reverse relations
   - Aggregation queries for statistics

3. **Caching Considerations:**
   - Analytics records cached via `RequestorBorrowerAnalytics`
   - Most requested items cached via `MostRequestedItem`
   - Activity logs immutable after creation

## Security

- **Access Control:**
  - Analytics pages restricted to Admin and GSO Staff only
  - Users can only view their own detailed analytics (future enhancement)
  - All views check user role before allowing access

- **Data Validation:**
  - Date range validation on both frontend and backend
  - Search term validation
  - User ID validation before queries

## Future Enhancements

1. **Department-Level Analytics:**
   - Track analytics by department
   - Compare departments

2. **Trend Analysis:**
   - Request/borrow trends over time
   - Seasonal patterns
   - Peak usage periods

3. **Advanced Reporting:**
   - Customizable report generation
   - Scheduled email reports
   - Dashboard widgets

4. **User-Specific Views:**
   - Allow users to view their own analytics
   - Personal request history with charts
   - Borrowing calendar

5. **Notifications:**
   - Alert when user becomes top requestor
   - Notification for overdue items
   - Weekly activity summary

6. **Charts & Graphs:**
   - Request trends over time
   - Item popularity charts
   - User activity heatmaps
   - Return rate visualizations

## Troubleshooting

### Analytics Not Showing
1. Run `python manage.py migrate` to apply schema
2. Run `python manage.py populate_analytics` for existing data
3. Check that user role is 'department_user'

### Export Not Working
1. Ensure ReportLab library is installed: `pip install reportlab`
2. Check file permissions on media directory
3. Verify CSRF token is included in form

### Signals Not Triggering
1. Verify `inventory.signals` is imported in `apps.py`
2. Check Django app configuration in `INSTALLED_APPS`
3. Verify signal receivers are connected properly

## Dependencies

- Django 3.2+
- ReportLab (for PDF export)
- Django ORM
- Bootstrap/Tailwind CSS (for styling)

## Installation

The analytics system is automatically integrated. To complete setup:

1. Run migrations:
   ```bash
   python manage.py migrate
   ```

2. Populate existing data:
   ```bash
   python manage.py populate_analytics
   ```

3. Restart Django development server:
   ```bash
   python manage.py runserver
   ```

4. Navigate to: Analytics menu in sidebar (for GSO/Admin users)

---

**Last Updated:** December 6, 2025
**Version:** 1.0
