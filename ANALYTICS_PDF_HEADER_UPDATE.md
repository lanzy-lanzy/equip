# Analytics PDF Export Header Update

## Summary
Updated the User Analytics PDF export to include professional institutional branding matching the other report exports.

## Files Modified

### `inventory/analytics_views.py`

1. **Import Update** (Line 15)
   - Added `Image` to reportlab.platypus imports

2. **Function Update** (Lines 489-577)
   - `export_analytics_pdf()` now includes:
     - Institutional logos (JH and IT)
     - Institution header: "J.H. CERILLES STATE COLLEGE"
     - Campus location: "Dumingag Campus"
     - Decorative green separator line
     - Improved title styling matching other reports

## What Was Added

### Header Components

1. **Logos**
   - JH Logo: 1.2" tall, maintains aspect ratio
   - IT Logo: 1.0" × 1.0" (perfectly round)

2. **Institution Information**
   - College Name: "J.H. CERILLES STATE COLLEGE" (Dark Green #1B5E20, 16pt)
   - Campus: "Dumingag Campus" (Medium Green #2E7D32, 13pt)
   - Separator: Dark green line

3. **Report Title**
   - "User Analytics Report - {username}"
   - Dark green color matching institution theme
   - Centered alignment

## Consistency

All PDF exports now use consistent branding:
- ✓ Supplies Report
- ✓ Supply Requests Report
- ✓ Inventory Transactions Report
- ✓ User Analytics Report

All exports feature:
- Same logo sizing and positioning
- Same institution header text and styling
- Same color scheme (dark/medium green)
- Same separator line styling
