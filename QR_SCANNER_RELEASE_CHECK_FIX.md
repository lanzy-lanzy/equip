# QR Scanner Release Status Check Fix

## Problem
When scanning an item in the QR code scanner, the system was not properly determining whether an item is "released" (borrowed but not yet returned) or not. This caused confusion about whether to show the "Issue" button or "Return" button.

**Expected Behavior:**
- If item is NOT released (never borrowed) → Show "Issue" button
- If item IS released (borrowed but not returned) → Show "Return" button

**Previous Issue:**
The frontend was checking transaction history to determine if an item was borrowed, but this method only checked if the most recent transaction was an "out" (issue), which doesn't distinguish between:
- An item that was issued but has already been returned
- An item that was issued and is still borrowed

## Solution

### Backend Change (views.py)
Modified `process_qr_scan` function to check the `BorrowedItem` model for active borrowed items:

```python
# Check if item is currently borrowed (released but not returned)
is_item_borrowed = False
borrowed_item = BorrowedItem.objects.filter(
    supply=supply,
    returned_at__isnull=True  # Item is borrowed if returned_at is null
).order_by('-borrowed_at').first()

if borrowed_item:
    is_item_borrowed = True
```

This checks if there's an active `BorrowedItem` record where `returned_at` is null, which indicates the item is still borrowed.

The response now includes:
```json
{
    "success": true,
    "supply": {...},
    "transaction_history": [...],
    "is_item_borrowed": true/false,  // NEW: Indicates if item is currently borrowed
    "message": "..."
}
```

### Frontend Change (qr_scanner.html)
Updated `fetchAndShowItemInfo` function to use the `is_item_borrowed` flag from the backend instead of checking transaction history:

**Before:**
```javascript
const isBorrowed = checkIfBorrowed(result.transaction_history);
if (isBorrowed) {
    showReturnConfirmationModal(result);
} else {
    showItemInfoModal(result);
}
```

**After:**
```javascript
if (result.is_item_borrowed) {
    showReturnConfirmationModal(result);
} else {
    showItemInfoModal(result);
}
```

## Flow Logic

1. **When scanning an item QR code:**
   - Backend queries `BorrowedItem` table
   - Checks if there's an unreturned borrowed record (`returned_at` is null)
   - Sends `is_item_borrowed` flag to frontend

2. **Frontend Decision:**
   - If `is_item_borrowed === true` → Show "Return Item" button (yellow modal)
   - If `is_item_borrowed === false` → Show item info with action buttons (Issue/Return/Scan)

3. **For Borrowing Request QR codes:**
   - Uses the `status` field of `SupplyRequest` (approved → Issue, released → Return)
   - This logic remains unchanged

## Testing

To test this fix:

1. Create a supply item
2. Create a borrowing request for the item
3. Issue the item via QR scanner (creates `BorrowedItem` record with `returned_at=null`)
4. Scan the item again → Should show "Return Item" button
5. Return the item via QR scanner (sets `returned_at=now()`)
6. Scan the item again → Should show item info with Issue/Return buttons

## Files Modified

- `c:/Users/CHAN/dev/supply_/inventory/views.py` - Added `is_item_borrowed` check
- `c:/Users/CHAN/dev/supply_/templates/inventory/qr_scanner.html` - Updated frontend logic to use `is_item_borrowed` flag

## Related Models

The fix relies on the `BorrowedItem` model which has:
- `supply`: ForeignKey to Supply
- `borrower`: ForeignKey to User
- `borrowed_at`: DateTime when borrowed
- `returned_at`: DateTime when returned (null if still borrowed)
- Other tracking fields

The `is_returned` property (if available in the model) returns `self.returned_at is not None`.
