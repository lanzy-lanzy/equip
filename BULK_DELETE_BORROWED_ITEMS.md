# Bulk Delete Borrowed Items Feature

## Overview
Implemented bulk deletion functionality for borrowed items in the GSO (General Services Office) staff interface. Allows GSO/Admin staff to select and delete multiple borrowed items at once.

## Changes Made

### 1. **Backend - View (views.py)**
Added new view function `bulk_delete_borrowed_items`:
- **Location**: `inventory/views.py` (lines 1790-1841)
- **Authentication**: Requires login, restricted to Admin and GSO staff roles
- **Functionality**:
  - Accepts POST requests with list of item IDs
  - For unreturned items: automatically restores supply quantity
  - Logs inventory transactions for all restored items
  - Supports both HTMX and regular form submissions
  - Returns appropriate JSON responses and messages

### 2. **Frontend - URL Route (urls.py)**
Added URL endpoint:
- **Location**: `inventory/urls.py` (line 50)
- **URL**: `borrowed-items/bulk-delete/`
- **Name**: `bulk_delete_borrowed_items`

### 3. **Frontend - Template (borrowed_items_list.html)**
Added bulk selection and action interface:

#### Bulk Action Toolbar (lines 4-22)
- Appears only when items are selected
- Shows count of selected items
- Provides quick action buttons:
  - "Select All" - Selects all checkboxes
  - "Deselect All" - Clears all selections
  - "Delete Selected" - Triggers bulk delete with confirmation

#### Table Enhancements (lines 27-30)
- Added checkbox column header (visible only to Admin/GSO staff)
- Master checkbox to toggle all item selections

#### Row Changes (lines 72-76)
- Added checkbox in first column of each row
- Updates selection count on checkbox changes

#### JavaScript Functions (lines 294-374)
- `updateSelectedCount()` - Updates toolbar visibility and selection count
- `toggleSelectAll(checkbox)` - Toggles all checkboxes based on master checkbox
- `selectAllItems()` - Manually selects all items
- `deselectAllItems()` - Manually deselects all items
- `deleteSelectedItems()` - Handles bulk delete process with:
  - Selection validation
  - Confirmation dialog
  - CSRF token handling
  - Page reload on success

### 4. **Base Template Enhancement (base.html)**
Added CSRF token in meta tag (line 14):
```html
<meta name="csrf-token" content="{{ csrf_token }}">
```

## Features

### Security
- ✅ CSRF protection via meta tag and X-CSRFToken header
- ✅ Role-based access control (Admin/GSO staff only)
- ✅ POST-only endpoint prevents accidental deletion via GET

### User Experience
- ✅ Checkbox selection on each row
- ✅ Master checkbox to select/deselect all items
- ✅ Dynamic toolbar that appears when items are selected
- ✅ Selection count display
- ✅ Confirmation dialog before deletion
- ✅ Success/error messages
- ✅ Automatic page reload to show updated list

### Data Integrity
- ✅ Automatically restores supply quantities for unreturned items
- ✅ Logs inventory transactions for audit trail
- ✅ Handles both returned and unreturned items appropriately

## Usage

1. **Navigate to Borrowed Items List**
   - Go to "Borrowed Items" from the sidebar

2. **Select Items for Deletion**
   - Click checkboxes next to items you want to delete
   - Use "Select All" button to select all visible items
   - Selection count updates in blue toolbar

3. **Perform Bulk Delete**
   - Click "Delete Selected" button in toolbar
   - Confirm the action in the dialog
   - System will delete selected items and refresh the list

## Notes
- Deletion cannot be undone
- Unreturned items will have their quantities restored to inventory
- All deletions are logged in inventory transactions for audit purposes
- Feature is only visible to Admin and GSO staff roles
- Department users cannot see or use bulk delete functionality
