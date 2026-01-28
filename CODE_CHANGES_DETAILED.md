# Detailed Code Changes - QR Scanner Issue/Return Fix

## File 1: `inventory/views.py` (Backend)

### Location: In `process_qr_scan()` function, around line 862

### Change: Add item borrowed status check

**Code Added (Before the final return statement):**

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

**Location in file:** Add this code block after line 905 (after the transaction history loop)

### Change: Add flag to JSON response

**Original Code:**
```python
return JsonResponse({
    'success': True,
    'supply': {
        'id': supply.id,
        'name': supply.name,
        'quantity': supply.quantity,
        'location': supply.location,
        'action': action,
        'timestamp': scan_log.timestamp.isoformat()
    },
    'transaction_history': transaction_history,
    'message': message
})
```

**Updated Code:**
```python
return JsonResponse({
    'success': True,
    'supply': {
        'id': supply.id,
        'name': supply.name,
        'quantity': supply.quantity,
        'location': supply.location,
        'action': action,
        'timestamp': scan_log.timestamp.isoformat()
    },
    'transaction_history': transaction_history,
    'is_item_borrowed': is_item_borrowed,  # <-- NEW LINE
    'message': message
})
```

---

## File 2: `templates/inventory/qr_scanner.html` (Frontend)

### Change 1: Update `fetchAndShowItemInfo()` function

**Location:** Around line 521-542

**Original Code:**
```javascript
} else {
    // Check if the item is currently borrowed by checking transaction history
    const isBorrowed = checkIfBorrowed(result.transaction_history);
    if (isBorrowed) {
        // Show return confirmation modal for borrowed items
        showReturnConfirmationModal(result);
    } else {
        // Show regular item info modal with action buttons
        showItemInfoModal(result);
    }
}
```

**Updated Code:**
```javascript
} else {
    // Check if the item is currently borrowed (using the is_item_borrowed flag from backend)
    if (result.is_item_borrowed) {
        // Show return confirmation modal for borrowed items
        showReturnConfirmationModal(result);
    } else {
        // Show regular item info modal with action buttons
        showItemInfoModal(result);
    }
}
```

**Key Change:** 
- Removed: `const isBorrowed = checkIfBorrowed(result.transaction_history);`
- Added: Direct check of `result.is_item_borrowed` flag from backend

---

### Change 2: Update `showItemInfoModal()` function

**Location:** Around line 641-676

**Original Code:**
```javascript
// Check if the item is currently borrowed (has an "out" transaction)
const isBorrowed = checkIfBorrowed(result.transaction_history);

if (isBorrowed) {
    // If borrowed, show only the Return button
    actionButtons = `
        <div class="mt-6">
            <button type="button" onclick="performModalAction('return')" 
                    class="w-full px-4 py-2 bg-yellow-600 text-white rounded-lg hover:bg-yellow-700 transition-colors">
                <i class="fas fa-arrow-down mr-2"></i>Return Item
            </button>
        </div>
    `;
} else {
    // If not borrowed, show both Issue and Return buttons
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

**Updated Code:**
```javascript
// Check if the item is currently borrowed using the is_item_borrowed flag from backend
// This is more reliable than checking transaction history
const isBorrowed = result.is_item_borrowed || checkIfBorrowed(result.transaction_history);

if (isBorrowed) {
    // If borrowed, show only the Return button
    actionButtons = `
        <div class="mt-6">
            <button type="button" onclick="performModalAction('return')" 
                    class="w-full px-4 py-2 bg-yellow-600 text-white rounded-lg hover:bg-yellow-700 transition-colors">
                <i class="fas fa-arrow-down mr-2"></i>Return Item
            </button>
        </div>
    `;
} else {
    // If not borrowed, show both Issue and Return buttons
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

**Key Changes:**
- Updated: `const isBorrowed = result.is_item_borrowed || checkIfBorrowed(result.transaction_history);`
  - Uses backend flag as primary check
  - Falls back to transaction history as secondary check (for backward compatibility)

---

## Summary of Changes

| File | Function | Change | Type |
|------|----------|--------|------|
| `views.py` | `process_qr_scan` | Add `is_item_borrowed` check | Added 9 lines |
| `views.py` | `process_qr_scan` | Add flag to response | Modified 1 line |
| `qr_scanner.html` | `fetchAndShowItemInfo` | Use `is_item_borrowed` flag | Modified 1 line |
| `qr_scanner.html` | `showItemInfoModal` | Use `is_item_borrowed` flag with fallback | Modified 1 line |

**Total Lines Changed:** ~15 lines
**Total Lines Added:** ~12 lines
**Complexity:** Low
**Risk Level:** Low (uses existing database fields, no migrations needed)
**Breaking Changes:** None

---

## Verification Checklist

After applying these changes, verify:

- [ ] Django migrations not needed (using existing fields)
- [ ] Server starts without errors
- [ ] QR scanner page loads without JavaScript errors
- [ ] Scanning an unborrowed item shows Issue/Return buttons
- [ ] Scanning a borrowed item shows only Return button
- [ ] Scanning a previously borrowed (now returned) item shows Issue/Return buttons
- [ ] Borrowing request QR codes still work correctly
- [ ] All transaction history displays correctly
- [ ] Error messages display correctly
