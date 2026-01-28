# Reports Filter & Search Implementation

## Overview
Implemented comprehensive filtering and search functionality for the Reports & Analytics page, allowing users to filter data by date range, search terms, and status before viewing or exporting to PDF/CSV.

## Features Implemented

### 1. Filter Panel UI
- **Location**: `/templates/inventory/reports.html`
- **Components**:
  - Search input (searches across supply names, request IDs, user names)
  - Date range picker (From Date and To Date)
  - Status filter dropdown (for requests: pending, approved, released, rejected)
  - Report type selector (Overview, Requests, Transactions, Supplies)
  - Apply Filters and Clear Filters buttons

### 2. Report Types
- **Overview**: Summary cards and charts (default view)
- **Requests**: Detailed table of supply requests with filters applied
- **Transactions**: Detailed table of inventory transactions with filters applied
- **Supplies**: Detailed table of supplies with filters applied

### 3. Dynamic Table Display
The filters immediately update the table content before export, allowing users to:
- Preview filtered data
- Verify results are correct
- Then export with confidence

### 4. Filter-Aware Exports
All export functions (CSV and PDF) now respect the applied filters:
- `export_supplies_csv()` - Supports search, date range filters
- `export_requests_csv()` - Supports search, date range, status filters
- `export_transactions_csv()` - Supports search, date range filters
- `export_supplies_pdf()` - Supports search, date range filters with filter info in PDF
- `export_requests_pdf()` - Supports search, date range, status filters with filter info in PDF
- `export_transactions_pdf()` - Supports search, date range filters with filter info in PDF

## Backend Implementation

### Views (`inventory/views.py`)

#### `reports()` View
Updated to:
- Accept filter parameters via GET request (search, date_from, date_to, status, report_type)
- Apply filters to querysets
- Support HTMX requests for dynamic table updates
- Return appropriate template based on report type

```python
@login_required
def reports(request):
    # Get filter parameters
    report_type = request.GET.get('report_type', 'overview')
    date_from = request.GET.get('date_from', '')
    date_to = request.GET.get('date_to', '')
    search_query = request.GET.get('search', '')
    status_filter = request.GET.get('status', '')
    
    # Apply filters to querysets
    filtered_requests = SupplyRequest.objects.all()
    filtered_transactions = InventoryTransaction.objects.all()
    filtered_supplies = Supply.objects.all()
    
    # Return HTMX partial or full page
    if request.htmx:
        if report_type == 'requests':
            return render(request, 'inventory/partials/reports_requests_table.html', context)
        # ... other report types
    
    return render(request, 'inventory/reports.html', context)
```

#### Export Functions Updated
All six export functions now:
1. Extract filter parameters from GET request
2. Apply filters to the querysets
3. Include filter information in the output (PDF headers show applied filters)
4. Convert numeric fields to strings for PDF compatibility

### Filter Logic
Filters work as follows:
- **Search**: Case-insensitive partial matching across relevant fields
- **Date Range**: 
  - From: Includes entire day (00:00:00)
  - To: Includes entire day by adding 1 day and using less-than comparison
- **Status**: Exact match filtering for request status
- **Combination**: Multiple filters applied together (AND logic)

## Frontend Implementation

### Main Template (`templates/inventory/reports.html`)
- Responsive filter form with 5 input fields in grid layout
- Integrated with HTMX for dynamic updates
- Clear and Apply filters buttons
- Conditional rendering of report type content

### Partial Templates

1. **`reports_requests_table.html`**
   - Table with columns: Request ID, User, Supply, Quantity, Status, Approved By, Created At
   - Status badges with color coding
   - Empty state message

2. **`reports_transactions_table.html`**
   - Table with columns: Supply, Type, Quantity, Previous, New, Performed By, Created At
   - Transaction type badges (Stock In/Out/Adjustment)
   - Empty state message

3. **`reports_supplies_table.html`**
   - Table with columns: Name, Category, Quantity, Min Stock, Status, Unit, Location, Cost/Unit, Created At
   - Stock status badges (In Stock/Low Stock/Out of Stock)
   - Empty state message

## URL Configuration
Routes remain unchanged in `urls.py`:
```python
path('reports/', views.reports, name='reports'),
path('reports/export/supplies/', views.export_supplies_csv, name='export_supplies_csv'),
path('reports/export/requests/', views.export_requests_csv, name='export_requests_csv'),
path('reports/export/transactions/', views.export_transactions_csv, name='export_transactions_csv'),
path('reports/export/supplies/pdf/', views.export_supplies_pdf, name='export_supplies_pdf'),
path('reports/export/requests/pdf/', views.export_requests_pdf, name='export_requests_pdf'),
path('reports/export/transactions/pdf/', views.export_transactions_pdf, name='export_transactions_pdf'),
```

## HTMX Integration
The filter form uses HTMX for dynamic updates:
```html
<form id="reports-filter-form" hx-get="{% url 'reports' %}" hx-target="#report-content" hx-swap="innerHTML">
```

This allows:
- Instant table updates without page reload
- Smooth user experience
- Progressive enhancement

## File Changes Summary

### New Files Created
1. `/templates/inventory/partials/reports_requests_table.html` - Requests report table partial
2. `/templates/inventory/partials/reports_transactions_table.html` - Transactions report table partial
3. `/templates/inventory/partials/reports_supplies_table.html` - Supplies report table partial

### Modified Files
1. `/inventory/views.py` - Updated reports view and all export functions
2. `/templates/inventory/reports.html` - Complete redesign with filter panel and dynamic content

## Testing Guide

### Manual Testing Steps

1. **View Reports Page**
   - Navigate to `/reports/`
   - Verify filter panel is visible with all controls

2. **Test Search Filter**
   - Enter a supply name in search box
   - Click "Apply Filters"
   - Verify table updates to show matching results
   - Test with requests, transactions, supplies report types

3. **Test Date Range Filter**
   - Select a "From Date"
   - Select a "To Date"
   - Click "Apply Filters"
   - Verify only records within date range appear

4. **Test Status Filter** (Requests only)
   - Select a status from dropdown
   - Click "Apply Filters"
   - Verify only requests with that status appear

5. **Test Report Type Selector**
   - Select different report types
   - Verify appropriate table displays

6. **Test Exports with Filters**
   - Apply filters
   - Click CSV export button
   - Verify CSV contains only filtered data
   - Repeat for PDF exports
   - Verify PDF includes filter information in header

7. **Test Clear Filters**
   - Apply some filters
   - Click "Clear Filters"
   - Verify all filters reset and full dataset shows

8. **Test Combined Filters**
   - Apply search AND date range AND status together
   - Verify results are correctly filtered by all criteria

## Performance Considerations
- Filters use Django ORM with `select_related()` and `filter()` for efficient queries
- No N+1 queries due to use of select_related()
- Large datasets may benefit from pagination (can be added later if needed)

## Future Enhancements
1. Add pagination for large result sets
2. Add column sorting by clicking headers
3. Add category filter for supplies
4. Add export format (JSON)
5. Add custom date format selection
6. Add saved filter presets
7. Add scheduling for automated exports
8. Add export to email functionality

## Accessibility Features
- All form inputs have proper labels
- Semantic HTML structure
- ARIA labels on badges for status indicators
- Keyboard navigation support via HTMX

## Browser Compatibility
Works on all modern browsers supporting:
- HTML5 date input
- CSS Grid
- HTMX (no IE11 support, but that's acceptable)
