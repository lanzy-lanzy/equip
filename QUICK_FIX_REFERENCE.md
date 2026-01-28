# QR Scanner Issue/Return Button Fix - Quick Reference

## What Was Fixed
The QR scanner now correctly determines whether to show the "Issue" or "Return" button based on whether an item is currently borrowed.

## Changes Made

### Backend (`inventory/views.py` - process_qr_scan function)
- Added check for active borrowed items: `BorrowedItem` records with `returned_at=null`
- Added `is_item_borrowed` flag to JSON response

### Frontend (`templates/inventory/qr_scanner.html`)
- Updated `fetchAndShowItemInfo()` to use `is_item_borrowed` flag
- Updated `showItemInfoModal()` to use `is_item_borrowed` for button display logic

## How It Works

**When you scan an item:**
1. Backend queries: "Is there an active borrowed record for this item?"
   - Checks: `SELECT * FROM BorrowedItem WHERE supply=X AND returned_at IS NULL`
   
2. Backend responds with `is_item_borrowed: true/false`

3. Frontend displays:
   - **If true** → "Confirm Return" modal (only shows Return button)
   - **If false** → "Item Information" modal (shows Issue and Return buttons)

## Testing the Fix

**Test Case 1 - Item Not Borrowed:**
```
Scan → Should see: "Issue Item" and "Return Item" buttons
```

**Test Case 2 - Item Currently Borrowed:**
```
1. Issue an item via QR scanner
2. Scan the same item again
3. Should see: Only "Return Item" button (yellow modal)
```

**Test Case 3 - Item Previously Borrowed (Already Returned):**
```
1. Issue an item via QR scanner
2. Return the item via QR scanner
3. Scan the item again
4. Should see: "Issue Item" and "Return Item" buttons (same as not borrowed)
```

## Key Database Fields Used

- `BorrowedItem.returned_at` → `null` = still borrowed, `datetime` = returned

## Status

✅ Backend changes: Done
✅ Frontend changes: Done
✅ Testing documentation: Done

Ready for testing and deployment!
