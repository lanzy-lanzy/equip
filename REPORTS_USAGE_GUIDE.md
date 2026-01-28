# Reports Filter & Search - Usage Guide

## Quick Start

### Accessing Reports
1. Click "Reports" in the sidebar menu
2. You'll see the Reports & Analytics page with a filter panel at the top

## Using the Filter Panel

### Search Filter
**What it does**: Searches across supply names, request IDs, and usernames

**How to use**:
1. Type in the search box (e.g., "pen", "REQ-20250101", "john")
2. Click "Apply Filters"
3. Results update to show matching items

**Example**: Search for "Laptop" to find all requests, transactions, or supplies related to laptops

### Date Range Filter
**What it does**: Filters data between two dates (inclusive)

**How to use**:
1. Click "From Date" field, select a start date
2. Click "To Date" field, select an end date
3. Click "Apply Filters"
4. Results show only records created within that date range

**Example**: 
- From: 2025-01-01
- To: 2025-01-31
- Shows all January 2025 records

### Status Filter
**What it does**: Shows only requests with a specific status (Requests report only)

**How to use**:
1. Click the "Status" dropdown
2. Select one: All Statuses, Pending, Approved, Released, or Rejected
3. Click "Apply Filters"
4. Results show only requests with that status

**Example**: Select "Pending" to see all requests waiting for approval

### Report Type Selector
**Options**:
- **Overview**: Summary cards and charts (default)
- **Requests**: Detailed table of supply requests
- **Transactions**: Detailed table of inventory transactions
- **Supplies**: Detailed table of supplies

**How to use**:
1. Click the "Report Type" dropdown
2. Select the type you want
3. The page instantly switches to that report view

## Combining Filters

You can use multiple filters together!

**Example**: Find all pending laptop requests from January 2025
1. Report Type: Requests
2. Search: "laptop"
3. From Date: 2025-01-01
4. To Date: 2025-01-31
5. Status: Pending
6. Click "Apply Filters"

## Viewing Filtered Results

### Tables
- **Requests Table**: Shows Request ID, User, Supply, Quantity, Status, Approved By, Created Date
- **Transactions Table**: Shows Supply, Type, Quantity changes, Who performed it, Date
- **Supplies Table**: Shows Name, Category, Quantity, Min Stock, Status, Unit, Location, Cost

### Status Badges
- **Yellow**: Pending (requests) or Low Stock (supplies)
- **Blue**: Approved (requests)
- **Green**: Released/In Stock
- **Red**: Rejected/Out of Stock

## Exporting Data

### With Filters Applied
1. Set up your filters as desired
2. Scroll down to "Export Reports" section
3. Choose format:
   - **CSV**: Opens in Excel, Numbers, or other spreadsheet software
   - **PDF**: Professional formatted report

**Note**: Exports include only filtered data - CSV shows rows matching your filters, PDF includes a "Filters Applied" header showing what was filtered

### Export Options Available
1. **Supplies Report** → CSV or PDF
2. **Requests Report** → CSV or PDF (includes filters used)
3. **Transactions Report** → CSV or PDF

## Clearing Filters

To reset everything:
1. Click the "Clear Filters" button
2. All filters are removed
3. Full dataset is displayed

## Common Workflows

### Weekly Status Report
1. Report Type: Requests
2. From Date: Start of week
3. To Date: End of week
4. Status: All
5. Click Apply Filters
6. Export as PDF for management

### Monthly Inventory Check
1. Report Type: Supplies
2. Search: (leave blank)
3. From Date: First day of month
4. To Date: Last day of month
5. Click Apply Filters
6. Review low stock items
7. Export as CSV

### Track Specific Item Movement
1. Report Type: Transactions
2. Search: (item name)
3. From Date: (start date)
4. To Date: (today)
5. Click Apply Filters
6. See complete history of that item

### Pending Approvals
1. Report Type: Requests
2. Status: Pending
3. From Date: (empty - shows all pending)
4. To Date: (empty)
5. Click Apply Filters
6. See all requests waiting for approval

## Tips & Tricks

**Quick Filter Reset**
- Instead of clicking "Clear Filters", just refresh the page (F5 or Cmd+R)
- Or click the "Reports" menu item again

**Date Format**
- Use the date picker (click the field) for easier selection
- Format is: YYYY-MM-DD (2025-01-15 for January 15, 2025)

**Partial Matches**
- Search is case-insensitive
- "pen" finds "Pen", "PEN", "pencil", "expendable"
- No wildcards needed

**Export Large Datasets**
- If you have 10,000+ records, CSV export is faster than PDF
- PDF formatting can take a few seconds for very large reports

**Finding Recent Changes**
- Leave From Date empty to show all records from start
- Set To Date to today for recent activity

## Troubleshooting

**No results showing?**
- Check that filters are correct
- Try clearing filters to see all data
- Check date format is YYYY-MM-DD

**Filters not applying?**
- Make sure to click "Apply Filters" button
- Check browser console (F12) for errors

**Export seems empty?**
- The filters may have excluded all records
- Try less restrictive filters
- Use CSV format first to verify data

**Date picker not working?**
- Try typing date directly in format YYYY-MM-DD
- Or update your browser to latest version

## Screen Layout

```
┌─ Reports & Analytics ────────────────────────────┐
│                                                   │
│ ┌─ Filter & Search ────────────────────────────┐ │
│ │ Search | From Date | To Date | Status | Type│ │
│ │ [Apply] [Clear]                              │ │
│ └──────────────────────────────────────────────┘ │
│                                                   │
│ ┌─ Overview / Requests / Transactions / Supplies│ │
│ │                                                 │
│ │ [Table with filtered results]                 │
│ │                                                 │
│ └─────────────────────────────────────────────── │
│                                                   │
│ ┌─ Export Reports ─────────────────────────────┐ │
│ │ [CSV] [PDF]  [CSV] [PDF]  [CSV] [PDF]       │ │
│ │ Supplies    Requests    Transactions        │ │
│ └──────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────┘
```

## Need Help?

- Check this guide for common workflows
- Contact your system administrator
- All filters respect your user role permissions
