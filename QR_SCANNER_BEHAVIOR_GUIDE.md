# QR Scanner Behavior - Before and After

## Scenario 1: Item That Has Never Been Borrowed

### BEFORE FIX
```
User scans item "Pen, 1 box"
↓
System shows BOTH buttons:
┌─────────────────────────────┐
│ Item Information             │
├─────────────────────────────┤
│ Pen, 1 box                  │
│ Current Stock: 100 units    │
│ Location: Main Storage      │
├─────────────────────────────┤
│ [Issue Item] [Return Item]  │  ← Both buttons visible
└─────────────────────────────┘
```

### AFTER FIX
✅ **SAME BEHAVIOR** (No change)
```
User scans item "Pen, 1 box"
↓
System shows BOTH buttons:
┌─────────────────────────────┐
│ Item Information             │
├─────────────────────────────┤
│ Pen, 1 box                  │
│ Current Stock: 100 units    │
│ Location: Main Storage      │
├─────────────────────────────┤
│ [Issue Item] [Return Item]  │  ← Both buttons visible
└─────────────────────────────┘
```

---

## Scenario 2: Item That Is Currently Borrowed

### BEFORE FIX (BROKEN)
```
User scans item "Laptop"
  (that was issued yesterday, still borrowed)
↓
System shows BOTH buttons (INCORRECT):
┌──────────────────────────────┐
│ Item Information              │
├──────────────────────────────┤
│ Laptop                       │
│ Current Stock: 1 unit        │
│ Location: Department A       │
├──────────────────────────────┤
│ [Issue Item] [Return Item]   │  ← WRONG! Only Return should show
└──────────────────────────────┘

Problem: User might click "Issue" but item is already borrowed
```

### AFTER FIX ✅
```
User scans item "Laptop"
  (that was issued yesterday, still borrowed)
↓
Backend checks: Is returned_at NULL in BorrowedItem table?
↓
YES → is_item_borrowed = true
↓
System shows ONLY Return button:
┌──────────────────────────────┐
│ Confirm Return               │
├──────────────────────────────┤
│ ℹ️  Borrowed Item Detected   │
├──────────────────────────────┤
│ Laptop                       │
│ Current Stock: 0 units       │
│ Location: Department A       │
├──────────────────────────────┤
│ This item is currently       │
│ borrowed and needs to be     │
│ returned.                    │
│                              │
│ [Return Item] [Cancel]       │  ← CORRECT! Only Return available
└──────────────────────────────┘
```

---

## Scenario 3: Item That Was Borrowed But Already Returned

### BEFORE FIX (INCORRECT)
```
User scans item "Printer"
  (was issued Monday, returned Tuesday)
↓
System checks transaction history:
  - Latest transaction is "in" (return)
  - But system looks for "out" (issue)
↓
Shows both buttons (but might be confusing):
┌──────────────────────────────┐
│ Item Information              │
├──────────────────────────────┤
│ Printer                       │
│ Current Stock: 1 unit        │
│ Location: Main Storage       │
├──────────────────────────────┤
│ Recent Transactions:         │
│ Returned - 1 unit            │
│ Issued - 1 unit              │
├──────────────────────────────┤
│ [Issue Item] [Return Item]   │  ← Confusing context
└──────────────────────────────┘
```

### AFTER FIX ✅
```
User scans item "Printer"
  (was issued Monday, returned Tuesday)
↓
Backend checks: Is returned_at NULL in BorrowedItem table?
↓
NO (returned_at = Tuesday 3:45 PM) → is_item_borrowed = false
↓
System shows both buttons (CORRECT - item is available):
┌──────────────────────────────┐
│ Item Information              │
├──────────────────────────────┤
│ Printer                       │
│ Current Stock: 1 unit        │
│ Location: Main Storage       │
├──────────────────────────────┤
│ Recent Transactions:         │
│ Returned - 1 unit            │
│ Issued - 1 unit              │
├──────────────────────────────┤
│ [Issue Item] [Return Item]   │  ← Clear context (item available)
└──────────────────────────────┘
```

---

## Technical Comparison

### Database Check

#### BEFORE: Transaction History Analysis
```
Problem: Reads transaction history to guess current state
├─ Pro: Works with existing data
└─ Con: Ambiguous (multiple "out" transactions = ?)

Example:
   Transaction 1: Issue 2 units  (out)
   Transaction 2: Issue 3 units  (out)
   Transaction 3: Return 2 units (in)
   Transaction 4: Return 3 units (in)
   
   Latest transaction is "in" (return)
   Is item borrowed? NO ✓
```

#### AFTER: Borrowed Item Status ✅
```
Solution: Reads BorrowedItem.returned_at directly
├─ Pro: Clear, unambiguous, efficient
└─ Con: Requires BorrowedItem records (already exist)

Example:
   SELECT * FROM BorrowedItem 
   WHERE supply_id = 5 AND returned_at IS NULL
   
   Results:
   - If any record found → is_item_borrowed = true
   - If no records → is_item_borrowed = false
   
   Simple and accurate!
```

---

## User Experience Timeline

### Before Fix
```
Day 1: Issue Laptop
       ↓
Day 2: Try to return Laptop
       Scan QR → See BOTH buttons (confusing which to click)
       Click "Return Item" ✓
       
Day 3: Item returned and available
       Scan QR → See BOTH buttons (same as Day 2, unclear state)
       
Day 5: Need to issue Laptop again
       Scan QR → See BOTH buttons (user might click Return by mistake!)
```

### After Fix
```
Day 1: Issue Laptop
       ↓
Day 2: Try to return Laptop
       Scan QR → See ONLY "Return Item" button (clear action)
       Click "Return Item" ✓
       
Day 3: Item returned and available
       Scan QR → See BOTH buttons (clear state change)
       
Day 5: Need to issue Laptop again
       Scan QR → See BOTH buttons (same as Day 3, user knows it's available)
       Click "Issue Item" ✓
```

---

## Data Flow Diagram

### BEFORE FIX
```
Scan Item
   ↓
Frontend: Check transaction history
   ↓
   ├─ Is latest transaction "out"? → Guess: Maybe borrowed
   └─ Is latest transaction "in"?  → Guess: Maybe available
   ↓
Show buttons based on guess
   ↓
Potential user confusion or error
```

### AFTER FIX ✅
```
Scan Item
   ↓
Backend: Query BorrowedItem table
   ├─ WHERE supply=X AND returned_at IS NULL
   ├─ Found? → is_item_borrowed = true
   └─ Not found? → is_item_borrowed = false
   ↓
Send is_item_borrowed flag to frontend
   ↓
Frontend: Use flag to display correct buttons
   ├─ If true → Show only "Return Item"
   └─ If false → Show "Issue Item" and "Return Item"
   ↓
Clear user interface, correct action shown
```

---

## Summary

| Aspect | Before Fix | After Fix |
|--------|------------|-----------|
| **Accuracy** | Guesses based on transactions | Checks actual state |
| **Clarity** | Ambiguous button display | Clear button display |
| **User Confusion** | HIGH - both buttons always | LOW - context-aware buttons |
| **Technical** | Complex logic | Simple flag check |
| **Reliability** | Can fail with complex history | Always correct |

✅ **Fix Status:** Ready for production use
