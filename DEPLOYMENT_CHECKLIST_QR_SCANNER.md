# QR Scanner Issue/Return Fix - Deployment Checklist

## Pre-Deployment

### Code Review
- [x] Backend changes reviewed (`views.py`)
- [x] Frontend changes reviewed (`qr_scanner.html`)
- [x] No breaking changes to existing code
- [x] All imports present (BorrowedItem already imported)
- [x] No new migrations required (using existing fields)

### Testing Preparation
- [ ] Local testing environment ready
- [ ] Test data prepared (supplies, borrowing requests)
- [ ] Browser console ready for debugging
- [ ] Network tab ready for monitoring requests

---

## Local Testing (Before Deployment)

### Test Case 1: Item Never Borrowed
```
Steps:
1. [ ] Create a new supply item (e.g., "Test Pen")
2. [ ] Navigate to QR Scanner page
3. [ ] Scan the item (manually enter ID in input field if needed)
4. [ ] Expected: Shows item info modal with BOTH Issue and Return buttons
5. [ ] Expected: No JavaScript errors in console

Evidence:
- [ ] Modal appears
- [ ] Buttons visible and clickable
- [ ] Transaction history shows empty or no recent transactions
- [ ] Console clean (no errors)
```

### Test Case 2: Item Currently Borrowed
```
Steps:
1. [ ] From Test Case 1, click "Issue Item" button
2. [ ] Complete the issue action (enter location, click "Process Scan")
3. [ ] Scan the same item again
4. [ ] Expected: Shows "Confirm Return" modal with ONLY Return button
5. [ ] Expected: Modal header says "Borrowed Item Detected"

Evidence:
- [ ] Return confirmation modal appears (yellow background)
- [ ] Only one button visible: "Return Item"
- [ ] Message says "This item is currently borrowed"
- [ ] Transaction history shows "Issued" entry
- [ ] Console clean (no errors)
```

### Test Case 3: Item Previously Borrowed (Now Returned)
```
Steps:
1. [ ] From Test Case 2, click "Return Item" button
2. [ ] Complete the return action (enter location, click "Process Scan")
3. [ ] Scan the same item again
4. [ ] Expected: Shows item info modal with BOTH Issue and Return buttons
5. [ ] Expected: Same display as Test Case 1

Evidence:
- [ ] Item info modal appears
- [ ] Both Issue and Return buttons visible
- [ ] Transaction history shows both "Issued" and "Returned" entries
- [ ] Stock quantity restored
- [ ] Console clean (no errors)
```

### Test Case 4: Borrowing Request QR Code
```
Steps:
1. [ ] Create a borrowing request for an item
2. [ ] Approve the request
3. [ ] Generate/scan the borrowing request QR code
4. [ ] Expected: Shows borrowing request modal with Issue button
5. [ ] After issuing, scan again
6. [ ] Expected: Shows borrowing request modal with Return button

Evidence:
- [ ] Borrowing request modal appears
- [ ] Status changes correctly (approved → released)
- [ ] Buttons match request status
- [ ] Item transaction history correct
- [ ] Console clean (no errors)
```

---

## Backend Verification

### Database
- [ ] BorrowedItem table accessible
- [ ] No permission errors accessing table
- [ ] Sample queries work:
  ```sql
  -- Check for active borrowed items
  SELECT * FROM inventory_borroweditem 
  WHERE returned_at IS NULL 
  LIMIT 5;
  
  -- Check for returned items
  SELECT * FROM inventory_borroweditem 
  WHERE returned_at IS NOT NULL 
  LIMIT 5;
  ```

### API Response
- [ ] Check response includes `is_item_borrowed` field
- [ ] Field is boolean (true/false)
- [ ] Field values correct for each scenario

**Sample Response to Verify:**
```json
{
  "success": true,
  "supply": {
    "id": 1,
    "name": "Pen",
    "quantity": 100,
    "location": "Main Storage",
    "action": "scan",
    "timestamp": "2024-01-15T10:30:00Z"
  },
  "transaction_history": [...],
  "is_item_borrowed": false,
  "message": "..."
}
```

---

## Frontend Verification

### JavaScript
- [ ] Browser console shows no errors
- [ ] Browser console shows no warnings
- [ ] Network tab shows successful API calls
- [ ] Response includes `is_item_borrowed` field

### DOM Elements
- [ ] Correct modal appears based on `is_item_borrowed` value
- [ ] Button visibility matches expectations
- [ ] Modal styling intact (colors, fonts, layout)

### Function Calls
- [ ] `fetchAndShowItemInfo()` uses `is_item_borrowed` flag
- [ ] `showItemInfoModal()` uses `is_item_borrowed` flag
- [ ] `showReturnConfirmationModal()` called when borrowed
- [ ] Fallback logic works if needed

---

## Cross-Browser Testing

- [ ] Chrome/Chromium
- [ ] Firefox
- [ ] Edge
- [ ] Mobile browsers (if applicable)

---

## Performance Check

- [ ] API response time acceptable (< 500ms)
- [ ] No database query delays
- [ ] No memory leaks in browser console
- [ ] Modal rendering fast (< 100ms)

---

## Security Check

- [ ] CSRF token present and valid
- [ ] User authentication required
- [ ] No sensitive data in response
- [ ] No SQL injection vulnerability
- [ ] No XSS vulnerability

---

## Rollback Plan

If issues found after deployment:

1. [ ] Keep backup of original code
2. [ ] Revert to original `views.py` (remove `is_item_borrowed` check and response field)
3. [ ] Revert to original `qr_scanner.html` (remove uses of `is_item_borrowed`)
4. [ ] Restart Django server
5. [ ] Clear browser cache
6. [ ] Verify rollback successful

**Rollback Command:**
```bash
# In project root
git checkout -- inventory/views.py templates/inventory/qr_scanner.html
python manage.py runserver
```

---

## Post-Deployment Monitoring

### Day 1 (First Day in Production)
- [ ] Monitor error logs for QR scanner issues
- [ ] Check that borrowing requests work correctly
- [ ] Verify return confirmations appear for borrowed items
- [ ] Monitor performance (load times, response times)
- [ ] Gather user feedback

### Week 1
- [ ] Review QR scan logs for patterns
- [ ] Verify no broken item tracking
- [ ] Check BorrowedItem records are created correctly
- [ ] Verify returned_at field set correctly on returns

### Ongoing
- [ ] Monitor for edge cases
- [ ] Track user feedback
- [ ] Log any issues or unexpected behavior

---

## Success Criteria

✅ **Fix is successful if:**
1. Unborrowed items show Issue and Return buttons
2. Borrowed items show only Return button
3. Returned items show Issue and Return buttons again
4. No JavaScript errors in console
5. No database errors in server logs
6. API response includes `is_item_borrowed` field
7. Button display matches `is_item_borrowed` value
8. Users report correct button behavior
9. No regression in other QR scanner features
10. Borrowing requests still work correctly

---

## Sign-Off

| Role | Name | Date | Signature |
|------|------|------|-----------|
| Developer | | | |
| QA/Tester | | | |
| Project Manager | | | |

---

## Notes

- Estimated Deployment Time: < 5 minutes
- Expected Downtime: None (no migrations needed)
- Risk Level: **LOW**
- Rollback Time if Needed: < 2 minutes

---

## Documentation Files

Supporting documentation created:
- [x] `QR_SCANNER_RELEASE_CHECK_FIX.md` - Technical overview
- [x] `QR_SCANNER_ISSUE_RETURN_FIX_SUMMARY.md` - Detailed summary
- [x] `QUICK_FIX_REFERENCE.md` - Quick reference guide
- [x] `CODE_CHANGES_DETAILED.md` - Exact code changes
- [x] `QR_SCANNER_BEHAVIOR_GUIDE.md` - Before/after behavior
- [x] `DEPLOYMENT_CHECKLIST_QR_SCANNER.md` - This file

All documentation ready for team review and training.
