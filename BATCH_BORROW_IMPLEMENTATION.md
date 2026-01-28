# Batch Borrow Request Feature Implementation

## Overview
Added a new batch borrowing feature that allows department users to request multiple equipment/material items at once with search functionality, similar to the supply request batch feature.

## What's New

### 1. Batch Borrow Request Page
- **URL**: `/borrow/request/batch/`
- **Access**: Department users only
- **Features**:
  - Search-based item selection with live filtering
  - Equipment and Materials tabs for filtering
  - Add multiple items to a list before submitting
  - Set borrow duration for all items (in days)
  - Add purpose/reason for borrowing
  - Optional location field
  - Dynamic table showing selected items
  - Remove items from list before submission

### 2. User Interface
Both single and batch modes are available:
- **Single Request** (`/borrow/request/`): Original form - one item at a time
- **Batch Request** (`/borrow/request/batch/`): New feature - multiple items

Navigation buttons allow easy switching between both modes.

### 3. Search Functionality
- Type-to-search with live dropdown
- 1 character: Shows items starting with that letter
- 3+ characters: Shows items containing the search term
- Displays available stock in real-time
- Separates Equipment and Materials

### 4. Data Handling
- Items are grouped by creation timestamp (within 5 seconds)
- Batch requests appear as single grouped row in history
- Shows all items in the batch with quantities
- Label shows "REQ-BATCH" for grouped requests
- Can be approved/rejected as a batch

## Files Modified/Created

### New Files
- `templates/inventory/request_borrow_batch.html` - Batch borrow form template

### Modified Files
- `inventory/views.py`:
  - Updated `request_borrow_item()` - Enhanced with separate equipment/material data
  - Added `request_borrow_batch()` - New view for batch borrowing
  
- `inventory/urls.py`:
  - Added route: `path('borrow/request/batch/', views.request_borrow_batch, name='request_borrow_batch')`

- `templates/inventory/request_borrow_item.html`:
  - Added "Batch Request" button in header

## How to Use

### For Department Users

1. **Navigate to Batch Borrow**:
   - From sidebar: "Request for Equipment" → click "Batch Request" button
   - Or directly: `/borrow/request/batch/`

2. **Select Items**:
   - Choose Equipment or Materials tab
   - Search for item name (type 1 letter or 3+ characters)
   - Select from dropdown results
   - Enter quantity needed
   - Click "Add to List"
   - Repeat for other items

3. **Configure Request**:
   - Set "Borrow Duration" (days)
   - Enter "Purpose of Borrowing" (required)
   - Optionally specify location

4. **Submit**:
   - Click "Submit Borrow Request"
   - Request appears in history as grouped batch
   - GSO staff receives notification

### For GSO Staff

- View batch requests in "All Requests" with "-BATCH" label
- All items in batch are shown in single row
- Approve/reject entire batch at once
- Or view individual items by clicking details

## Technical Details

### Backend Processing
```python
request_borrow_batch():
- Validates user has no overdue items
- Collects supply_ids and quantities from form
- Creates separate SupplyRequest for each item
- All requests created within same second (grouped)
- Generates QR codes for tracking
- Purpose includes duration and batch marker
```

### Frontend Features
- JavaScript search filtering
- Real-time availability display
- Set tracking with add/remove functionality
- Form validation before submission
- Prevents duplicate items in list
- Dropdown auto-close on selection

## Data Structure

Items are passed as JSON from backend:
```json
{
  "id": 1,
  "name": "Laptop",
  "stock": 5,
  "unit": "pieces",
  "category": "Equipment",
  "location": "Storage Room"
}
```

## Notes

- Batch requests work seamlessly with existing approval workflow
- QR codes generated for tracking
- History grouping works same as supply request batches
- Overdue items check prevents new borrows
- All validations and permissions enforced
- Compatible with existing borrowing system

## Future Enhancements
- Add checklist to verify items on collection
- Email notifications for batch status
- Advanced scheduling for multiple batches
- Return tracking for batch items
