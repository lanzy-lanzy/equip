# Reports Filter Implementation - Quick Reference

## Implementation Summary

**What**: Full-featured filtering and search system for Reports page
**Where**: `/reports/` endpoint
**Who**: Admin and GSO Staff users
**Why**: Enable users to find specific data and export filtered results

## Key Files Modified

| File | Changes | Lines |
|------|---------|-------|
| `inventory/views.py` | Updated reports() view + 6 export functions | ~300 |
| `templates/inventory/reports.html` | Complete rewrite with filter panel | ~240 |
| `templates/inventory/partials/reports_requests_table.html` | NEW - Requests table partial | 45 |
| `templates/inventory/partials/reports_transactions_table.html` | NEW - Transactions table partial | 45 |
| `templates/inventory/partials/reports_supplies_table.html` | NEW - Supplies table partial | 47 |

## Filter Parameters (GET Query)

```python
# All supported filter parameters:
request.GET.get('search')           # Text search
request.GET.get('date_from')        # Start date (YYYY-MM-DD)
request.GET.get('date_to')          # End date (YYYY-MM-DD)
request.GET.get('status')           # Request status
request.GET.get('report_type')      # overview|requests|transactions|supplies
```

## Filter Logic (Pseudo Code)

```python
# Search (case-insensitive, partial match)
if search_query:
    queryset = queryset.filter(
        Q(field1__icontains=search_query) |
        Q(field2__icontains=search_query) |
        Q(field3__icontains=search_query)
    )

# Date Range (inclusive both ends)
if date_from:
    queryset = queryset.filter(created_at__gte=date_from_obj)
if date_to:
    queryset = queryset.filter(created_at__lt=date_to_obj + 1day)

# Status (exact match)
if status_filter:
    queryset = queryset.filter(status=status_filter)
```

## View Function Flow

```
reports(request)
    │
    ├─→ Extract filter parameters from GET
    │
    ├─→ Apply filters to querysets (3 querysets)
    │   - filtered_requests
    │   - filtered_transactions
    │   - filtered_supplies
    │
    ├─→ Build context dictionary
    │
    ├─→ Check if HTMX request
    │   ├─→ YES: Return partial template
    │   └─→ NO: Return full page template
    │
    └─→ Return response
```

## Export Function Pattern

```python
@login_required
def export_REPORTTYPE_FORMAT(request):
    # 1. Check permissions
    if request.user.role not in ['admin', 'gso_staff']:
        return redirect('dashboard')
    
    # 2. Extract filters from GET params
    search = request.GET.get('search', '')
    date_from = request.GET.get('date_from', '')
    date_to = request.GET.get('date_to', '')
    status = request.GET.get('status', '')  # For requests only
    
    # 3. Get base queryset
    queryset = Model.objects.all()
    
    # 4. Apply filters
    if search:
        queryset = queryset.filter(Q(...) | Q(...))
    if date_from:
        queryset = queryset.filter(created_at__gte=parse_date(date_from))
    if date_to:
        queryset = queryset.filter(created_at__lt=parse_date(date_to)+1day)
    if status:
        queryset = queryset.filter(status=status)
    
    # 5. Generate export (CSV or PDF)
    # For CSV: Create HttpResponse with CSV content
    # For PDF: Create PDF document with table
    
    # 6. Return response
    return response
```

## URL Patterns (No Changes)

```python
path('reports/', views.reports, name='reports'),
path('reports/export/supplies/', views.export_supplies_csv, name='export_supplies_csv'),
path('reports/export/requests/', views.export_requests_csv, name='export_requests_csv'),
path('reports/export/transactions/', views.export_transactions_csv, name='export_transactions_csv'),
path('reports/export/supplies/pdf/', views.export_supplies_pdf, name='export_supplies_pdf'),
path('reports/export/requests/pdf/', views.export_requests_pdf, name='export_requests_pdf'),
path('reports/export/transactions/pdf/', views.export_transactions_pdf, name='export_transactions_pdf'),
```

## Form Structure (HTML)

```html
<form hx-get="{% url 'reports' %}" hx-target="#report-content" hx-swap="innerHTML">
    <!-- Input Fields -->
    <input type="text" name="search" />
    <input type="date" name="date_from" />
    <input type="date" name="date_to" />
    <select name="status">
        <option value="">All</option>
        <option value="pending">Pending</option>
        <!-- ... -->
    </select>
    <select name="report_type">
        <option value="overview">Overview</option>
        <!-- ... -->
    </select>
    
    <!-- Actions -->
    <button type="submit">Apply Filters</button>
    <a href="{% url 'reports' %}">Clear Filters</a>
</form>
```

## HTMX Configuration

```html
<!-- Dynamic form submission -->
hx-get="{% url 'reports' %}"              <!-- Endpoint -->
hx-target="#report-content"               <!-- Where to put response -->
hx-swap="innerHTML"                       <!-- How to insert (replace content) -->

<!-- In view: Check if HTMX -->
if request.htmx:                          <!-- Detect HTMX request -->
    return render(request, 'partial.html')  <!-- Return partial only -->
```

## Template Context Variables

```python
context = {
    # Filter values (for form repopulation)
    'search_query': search_query,
    'date_from': date_from,
    'date_to': date_to,
    'status_filter': status_filter,
    'report_type': report_type,
    
    # Filtered data
    'filtered_requests': filtered_requests,
    'filtered_transactions': filtered_transactions,
    'filtered_supplies': filtered_supplies,
    
    # Summary stats
    'total_supplies': total_supplies,
    'low_stock_items': low_stock_items,
    'total_requests': total_requests,
    'pending_requests': pending_requests,
    'released_requests': released_requests,
    
    # Select options
    'request_statuses': SupplyRequest.STATUS_CHOICES,
}
```

## Common SQL Queries Generated

```sql
-- Search filter example
SELECT * FROM supply WHERE name LIKE '%pen%' OR description LIKE '%pen%'

-- Date range example
SELECT * FROM supply_request 
WHERE created_at >= '2025-01-01' AND created_at < '2025-02-01'

-- Combined filters
SELECT * FROM supply_request 
WHERE (request_id LIKE '%REQ%' OR supply_name LIKE '%pen%')
  AND status = 'pending'
  AND created_at >= '2025-01-01'

-- With select_related (optimized)
SELECT * FROM supply_request sr
JOIN user u ON sr.user_id = u.id
JOIN supply s ON sr.supply_id = s.id
WHERE sr.status = 'pending'
```

## Testing Commands

```bash
# Run Django checks
python manage.py check

# Run tests (if available)
python manage.py test

# Test with Django shell
python manage.py shell
>>> from inventory.models import SupplyRequest
>>> from django.db.models import Q
>>> # Test filters manually
>>> qs = SupplyRequest.objects.filter(Q(request_id__icontains='REQ'))
>>> qs.count()
```

## URL Examples (with filters)

```
# Base report
/reports/

# Search filter
/reports/?search=laptop

# Date range
/reports/?date_from=2025-01-01&date_to=2025-01-31

# Status filter (requests only)
/reports/?status=pending

# Report type
/reports/?report_type=requests

# Combined
/reports/?report_type=requests&status=pending&date_from=2025-01-01&search=laptop

# Export with filters
/reports/export/requests/?status=pending&date_from=2025-01-01&date_to=2025-01-31

# PDF export with filters
/reports/export/requests/pdf/?search=laptop&status=approved
```

## Browser Console Debugging

```javascript
// Check HTMX attributes are present
document.querySelector('[hx-get]')

// Monitor HTMX requests
htmx.logger = htmx.logger.debugLog

// Manually trigger filter form
document.getElementById('reports-filter-form').submit()
```

## Performance Tips

1. **For Large Datasets (>10k records)**
   - Add pagination
   - Implement caching
   - Use database indexes

2. **For Slow Exports**
   - Use CSV before PDF
   - Reduce date range
   - Consider async processing

3. **For Slow Searches**
   - Use full-text search on large text fields
   - Add database indexes on searched fields
   - Implement result limits

## Security Considerations

```python
# XSS Protection
# ✓ All user input escaped in templates
# ✓ No raw HTML in context variables

# SQL Injection Protection
# ✓ Using Django ORM (parameterized queries)
# ✓ No string concatenation in SQL

# Permission Control
# ✓ @login_required decorator on all views
# ✓ Role check at view level
# ✓ No data filtering by user (all authorized data visible)

# CSRF Protection
# ✓ Forms include CSRF token
# ✓ POST requests for state changes (if added later)
```

## Troubleshooting Guide

| Issue | Cause | Solution |
|-------|-------|----------|
| Filters not working | Missing HTMX library | Check base.html includes HTMX |
| Empty results | Filters too restrictive | Clear filters, check data exists |
| Wrong data showing | Context variable typo | Check template variable names |
| Export empty | All data filtered out | Verify filter parameters |
| Date not working | Wrong date format | Use YYYY-MM-DD format |
| Status filter missing | Not in requests report | Status filter only for requests |
| PDF header too long | Too many filters | Filters are truncated in PDF |

## Customization Points

### To Add New Search Field
```python
# In reports() view
filtered_requests = filtered_requests.filter(
    Q(...) |
    Q(new_field__icontains=search_query)  # Add here
)
```

### To Add New Filter Type
```python
# In reports() view
new_filter = request.GET.get('new_filter', '')
if new_filter:
    filtered_requests = filtered_requests.filter(field=new_filter)

# In template
<select name="new_filter">
    <option value="">All</option>
    <option value="value1">Label 1</option>
</select>

# In context
'new_filter_options': Model.FILTER_CHOICES,
```

### To Change Table Columns
Edit the partial templates:
```html
<!-- In reports_requests_table.html -->
<th>New Column Name</th>

<!-- In loop -->
<td>{{ request.new_field }}</td>
```

## Version Control

```bash
# Files to commit
git add inventory/views.py
git add templates/inventory/reports.html
git add templates/inventory/partials/reports_*.html
git add REPORTS_*.md

# Commit message
git commit -m "feat: Add comprehensive filtering and search to Reports page"

# No database migrations needed
# No dependencies changed
```

## Documentation Files

1. **REPORTS_FILTER_IMPLEMENTATION.md** - Full technical details
2. **REPORTS_USAGE_GUIDE.md** - End-user documentation
3. **REPORTS_CHANGES_SUMMARY.md** - Overview of all changes
4. **REPORTS_FEATURE_VISUAL_GUIDE.md** - UI/UX visual guide
5. **REPORTS_QUICK_REFERENCE.md** - This file

## Support Contacts

For issues or questions:
1. Check documentation files first
2. Review code comments in views.py
3. Check Django error logs
4. Verify database has sample data
5. Test with browser console (F12)

## Next Steps

After deploying:
1. Train users on filter functionality
2. Gather feedback on UX
3. Monitor performance with real data
4. Plan future enhancements (pagination, sorting, etc.)
5. Update help documentation with screenshots
