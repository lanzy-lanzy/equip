# PDF Header Improvement - JHCSC Duminga Campus

## Summary of Changes

Enhanced the PDF export headers across all reports to include professional institutional branding for JHCSC Duminga Campus.

## Files Modified

### `inventory/views.py`

Updated three PDF export functions:

1. **`export_supplies_pdf()` - Lines 2058-2112**
2. **`export_requests_pdf()` - Lines 2265-2319**
3. **`export_transactions_pdf()` - Lines 2467-2521**

## Header Improvements

### What Was Added

Each PDF export now includes:

1. **Institution Name Header**
   - Text: "J.H. CERILLES STATE COLLEGE"
   - Style: 16pt, Dark Green (#1B5E20), Bold, Centered

2. **Campus Location**
   - Text: "Dumingag Campus"
   - Style: 13pt, Medium Green (#2E7D32), Bold, Centered

3. **Separator Line**
   - Dark green horizontal line for visual separation

4. **Report Title**
   - Improved styling with dark green color
   - Changed font size to 14pt for better hierarchy
   - Now appears below institution/campus information

### Color Scheme
- **Primary Green**: #1B5E20 (Dark green - matches institution colors)
- **Secondary Green**: #2E7D32 (Medium green - accent color)
- Professional and cohesive with the provided logos

## Updated Report Titles

- **Supplies Report** → "Equipment & Supplies Inventory Report"
- **Supply Requests Report** (unchanged)
- **Inventory Transactions Report** (unchanged)

## Visual Hierarchy

```
┌─────────────────────────────────────┐
│   J.H. CERILLES STATE COLLEGE       │
├─────────────────────────────────────┤
│   Dumingag Campus                   │
├─────────────────────────────────────┤ ← Separator
│   Report Title                      │
│                                     │
│   Filters Applied: ...              │
│                                     │
│   [Data Table]                      │
└─────────────────────────────────────┘
```

## Benefits

✓ Professional institutional branding
✓ Clear campus identification
✓ Improved visual hierarchy
✓ Consistent formatting across all reports
✓ Better document appearance for official use
✓ Green color scheme matches institutional identity
