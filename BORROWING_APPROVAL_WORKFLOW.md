# Borrowing Approval Workflow

## Overview
The borrowing system now requires GSO staff approval. Department users submit a request, GSO staff reviews it, and then sets the specific borrow date and return deadline.

## New Workflow

### 1. Department User Submits Borrow Request
- **URL**: `/borrow/request/`
- **Form**: `BorrowRequestForm`
- **Fields**:
  - Supply (item to borrow)
  - Quantity (how many)
  - Purpose (why they need it)
  - Borrow Duration (default: 3 days)

- **Process**:
  1. User selects item, quantity, and purpose
  2. User specifies how long they want to borrow (default 3 days)
  3. System creates a SupplyRequest with status `pending` and marks it as `[BORROWING]`
  4. System generates a borrowing QR code
  5. User is redirected to request detail page

### 2. GSO Staff Reviews & Approves
- **In Request List**: GSO staff sees the borrow request like any other request
- **Click Approve**: Clicking approve on a borrow request redirects to `/borrow/approve/<id>/`

### 3. GSO Staff Sets Dates (New Step)
- **URL**: `/borrow/approve/<pk>/`
- **Form**: `BorrowedItemForm`
- **Fields**:
  - Borrow Date (when the item is being borrowed)
  - Duration (number of days - defaults to requested duration)
  - Location (where the item is from)
  - Notes (optional additional info)

- **Process**:
  1. GSO staff sees the request details
  2. GSO staff sets the borrow date (usually today)
  3. GSO staff confirms or adjusts the duration
  4. System calculates return deadline automatically
  5. GSO staff clicks "Approve & Create Borrow Record"

### 4. System Creates Borrow Record
- **Automatic Actions**:
  1. Creates `BorrowedItem` record with:
     - Supply
     - Borrower
     - Borrow date
     - Return deadline (auto-calculated)
     - Duration
  2. Updates SupplyRequest status to `released`
  3. Reduces supply quantity by borrowed amount
  4. Logs inventory transaction
  5. Success message shows borrower and return deadline

### 5. User Sees Borrowed Item
- Item appears in "My Borrowed Items" or borrowed items list
- Shows borrow date and return deadline clearly
- User can track when to return it

## Files Changed

### Forms (inventory/forms.py)
1. **BorrowRequestForm** (NEW)
   - Used by department users to submit borrow requests
   - Fields: supply, quantity_requested, purpose, borrow_duration_days
   - Generates a SupplyRequest with [BORROWING] marker

2. **BorrowedItemForm** (UPDATED)
   - Used by GSO staff to set dates during approval
   - Fields: borrowed_date, borrow_duration_days, location_when_borrowed, notes
   - Supply, borrower, quantity are set automatically by the view

### Views (inventory/views.py)
1. **request_approve** (UPDATED)
   - Now redirects borrowing requests to the new approve view instead of directly approving

2. **approve_borrow_request** (NEW)
   - GSO-only endpoint for approving borrow requests with date selection
   - Creates BorrowedItem record when form is submitted
   - Handles all inventory updates and transactions

3. **request_borrow_item** (UPDATED)
   - Now uses `BorrowRequestForm` instead of creating BorrowedItem directly
   - Creates a pending SupplyRequest for GSO approval
   - Generates borrowing QR code

### Templates
1. **request_borrow_item.html** (UPDATED)
   - Shows form for department users to submit borrow requests
   - Explains that GSO approval is required
   - No date selection at this stage

2. **approve_borrow_request.html** (NEW)
   - Shows request details and allows GSO staff to set dates
   - Real-time calculation of return deadline
   - Confirmation of all details before approval

### URLs (inventory/urls.py)
- Added: `path('borrow/approve/<int:pk>/', views.approve_borrow_request, name='approve_borrow_request')`

## Workflow Diagram

```
Department User
    |
    v
Submit Borrow Request (request_borrow_item)
    |
    v (creates SupplyRequest with [BORROWING])
    |
GSO Staff Reviews
    |
    v
Click Approve (redirects to approve_borrow_request)
    |
    v
Set Borrow Date & Return Deadline
    |
    v
Confirm & Create Borrow Record
    |
    v (creates BorrowedItem)
    |
User can now see borrowed item with return deadline
```

## Key Changes

### Request Status Flow
- **Before**: Pending → Approved → Released (auto on approval)
- **After**: Pending → (redirect to date form) → Released (when dates set)

### BorrowedItem Creation
- **Before**: Created when user submitted request
- **After**: Created when GSO staff approves and sets dates

### Date Control
- **Before**: User specified dates at request time
- **After**: GSO staff specifies dates at approval time

## Benefits

1. **Better Control**: GSO staff has full control over when the borrow period starts
2. **Flexibility**: Duration can be adjusted by GSO staff
3. **Clear Dates**: No ambiguity about when the borrow started
4. **Audit Trail**: All approval by GSO staff with timestamps
5. **Override**: GSO can adjust duration if needed during approval

## Testing the Feature

### As Department User:
1. Navigate to "Borrow Item"
2. Select an item, quantity, and purpose
3. Specify how long you need (default 3 days)
4. Click "Submit Borrow Request"
5. See the request in pending state

### As GSO Staff:
1. Go to "Requests" page
2. Find the borrow request
3. Click "Approve"
4. You're taken to approval page
5. Set borrow date (defaults to today)
6. Confirm duration
7. Click "Approve & Create Borrow Record"
8. Request is marked as released
9. BorrowedItem record is created

### Verify:
1. User sees item in "My Borrowed Items"
2. Shows borrow date and return deadline
3. Supply quantity has been reduced
4. Inventory transaction is logged

## Error Handling

- If request is not pending: Shows error "Request already processed"
- If not a borrowing request: Shows error "This is not a borrowing request"
- If form validation fails: Shows errors for specific fields
- If insufficient stock: Form validation would catch this (happens at request level)
