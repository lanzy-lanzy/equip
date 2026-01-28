# QR Scanner Issue/Return Button Fix - Summary

## Problem Statement
When scanning an item in the QR code scanner in GSO (Goods Supply Office), the system was not properly checking if an item has been **released** (borrowed) or not before showing the appropriate action button. 

**Current Issue:**
- System shows both "Issue" and "Return" buttons for all non-borrowed items
- System doesn't properly distinguish between:
  - Items that have never been borrowed
  - Items that were borrowed and already returned
  - Items that are currently borrowed (released but not yet returned)

**Required Behavior:**
- If item is NOT released (never borrowed or already returned) → Show "Issue" button
- If item IS released (currently borrowed) → Show "Return" button

## Solution Overview

The fix involves two main changes:

### 1. Backend Change - `inventory/views.py`

Modified the `process_qr_scan` function to check the `BorrowedItem` model to determine if an item is currently borrowed.

**Added Logic:**
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

**Key Point:** The `BorrowedItem.returned_at` field being `null` indicates the item is still borrowed. Once returned, this field is set to the return datetime.

**Modified Response:**
The JSON response now includes:
```json
{
    "success": true,
    "supply": { /* ... */ },
    "transaction_history": [ /* ... */ ],
    "is_item_borrowed": true/false,  // NEW FLAG
    "message": "..."
}
```

### 2. Frontend Change - `templates/inventory/qr_scanner.html`

Updated two functions:

#### a) `fetchAndShowItemInfo()` - Primary Item Scanning
Changed the logic to use the new `is_item_borrowed` flag from backend:

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
    showReturnConfirmationModal(result);  // Show Return button
} else {
    showItemInfoModal(result);  // Show Issue/Return buttons
}
```

#### b) `showItemInfoModal()` - Fallback Logic
Updated button display logic to use `is_item_borrowed` flag as primary check:

```javascript
const isBorrowed = result.is_item_borrowed || checkIfBorrowed(result.transaction_history);

if (isBorrowed) {
    // Show only Return button
    actionButtons = `
        <div class="mt-6">
            <button type="button" onclick="performModalAction('return')" 
                    class="w-full px-4 py-2 bg-yellow-600 text-white rounded-lg hover:bg-yellow-700 transition-colors">
                <i class="fas fa-arrow-down mr-2"></i>Return Item
            </button>
        </div>
    `;
} else {
    // Show both Issue and Return buttons
    actionButtons = `
        <div class="mt-6 flex space-x-3">
            <button type="button" onclick="performModalAction('issue')" 
                    class="flex-1 px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors">
                <i class="fas fa-arrow-up mr-2"></i>Issue Item
            </button>
            <button type="button" onclick="performModalAction('return')" 
                    class="flex-1 px-4 py-2 bg-yellow-600 text-white rounded-lg hover:bg-yellow-700 transition-colors">
                <i class="fas fa-arrow-down mr-2"></i>Return Item
            </button>
        </div>
    `;
}
```

## Complete Flow Diagram

```
1. Scan QR Code
   ↓
2. Frontend sends scan request to backend with action='scan'
   ↓
3. Backend:
   - Gets supply item
   - Checks BorrowedItem table for unreturned items:
     * WHERE supply=item AND returned_at IS NULL
   - Sets is_item_borrowed = true/false
   - Returns JSON with is_item_borrowed flag
   ↓
4. Frontend receives response:
   - If is_item_borrowed = true:
     → Show "Confirm Return" modal with only "Return Item" button
   - If is_item_borrowed = false:
     → Show "Item Information" modal with both "Issue Item" and "Return Item" buttons
   ↓
5. User clicks appropriate button
   ↓
6. Perform action (Issue/Return)
```

## Test Scenarios

### Scenario 1: Item Never Borrowed
1. Create a supply item (e.g., "Pen, 1 box")
2. Scan the item
3. **Expected:** Shows "Item Information" modal with "Issue Item" and "Return Item" buttons

### Scenario 2: Item Issued and Currently Borrowed
1. Create a borrowing request for an item
2. Scan and issue the item (creates `BorrowedItem` record with `returned_at=null`)
3. Scan the same item again
4. **Expected:** Shows "Confirm Return" modal with only "Return Item" button

### Scenario 3: Item Previously Borrowed and Returned
1. Issue an item (from scenario 2)
2. Return the item (sets `returned_at=now()`)
3. Scan the item again
4. **Expected:** Shows "Item Information" modal with "Issue Item" and "Return Item" buttons
   (Same as Scenario 1 because item is no longer actively borrowed)

## Files Modified

1. **`c:/Users/CHAN/dev/supply_/inventory/views.py`**
   - Added `is_item_borrowed` check in `process_qr_scan()` function
   - Added `is_item_borrowed` to JSON response

2. **`c:/Users/CHAN/dev/supply_/templates/inventory/qr_scanner.html`**
   - Updated `fetchAndShowItemInfo()` to use `is_item_borrowed` flag
   - Updated `showItemInfoModal()` to use `is_item_borrowed` flag for button display

## Database Queries

The fix relies on checking the `BorrowedItem` model:

```sql
-- Check if item is currently borrowed
SELECT * FROM inventory_borroweditem
WHERE supply_id = ? AND returned_at IS NULL
ORDER BY borrowed_at DESC
LIMIT 1;
```

## No Breaking Changes

- The `checkIfBorrowed()` function is kept as a fallback
- Transaction history display remains unchanged
- Borrowing request QR code logic is unchanged
- All existing functionality is preserved

## Benefits

1. **Accuracy:** Uses database state (`returned_at` field) instead of transaction history
2. **Simplicity:** Single boolean flag instead of complex transaction logic
3. **Reliability:** Distinguishes between "never borrowed", "borrowed and returned", and "currently borrowed"
4. **Maintainability:** Easier to understand and debug in the future
5. **Performance:** Direct database query vs analyzing transaction history

## Notes

- The fix assumes `BorrowedItem` records are created whenever an item is issued
- The fix assumes `returned_at` is set when an item is returned
- The fix handles both regular QR codes and borrowing request QR codes
- Borrowing request QR codes still use the `status` field (approved/released) for button logic
