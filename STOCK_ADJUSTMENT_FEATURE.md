# Stock Adjustment Feature - Lost/Damaged Items

## Overview
This feature allows GSO staff and admins to record and track inventory adjustments for lost or damaged items. It maintains a complete audit trail of all adjustments made to the inventory.

## Features Implemented

### 1. Model Changes
- Updated `InventoryTransaction` model to support two new transaction types:
  - `'lost'` - For items that went missing
  - `'damaged'` - For items that are no longer usable

### 2. Forms
- **StockAdjustmentForm** - A custom form for creating stock adjustments with:
  - Supply selection dropdown
  - Adjustment type (Lost/Damaged)
  - Quantity affected
  - Detailed reason/description

### 3. Views
Three new views in `stock_adjustment_views.py`:

#### `stock_adjustment_list`
- Lists all stock adjustments (lost/damaged items)
- Filter by supply, type, or search term
- Displays statistics (total lost, total damaged)
- Pagination support for large datasets
- Shows adjustment details in a table format

#### `stock_adjustment_create`
- Form to record a new stock adjustment
- Validates that sufficient quantity is available
- Automatically updates supply quantity
- Creates transaction record for audit trail

#### `stock_adjustment_detail`
- Shows detailed information about a specific adjustment
- Displays affected item details
- Shows stock impact (before/after)
- Displays loss value calculation
- Shows who recorded it and when

### 4. Templates
Three new templates created:

#### `stock_adjustment_list.html`
- Statistics cards showing total, lost, and damaged counts
- Advanced filtering (by supply, type, search)
- Table view of all adjustments
- Pagination controls
- Quick action buttons to view details

#### `stock_adjustment_form.html`
- Clean form layout with sections
- Type selection with visual indicators
- Supply selection dropdown
- Quantity and reason inputs
- Submit and cancel buttons

#### `stock_adjustment_detail.html`
- Complete adjustment details
- Supply information and image
- Adjustment metrics (quantity, before/after stock)
- Loss value calculation
- Recorded by information
- Date and time of adjustment

### 5. URL Routes
Added three new URL patterns:
```python
path('stock-adjustments/', stock_adjustment_views.stock_adjustment_list, name='stock_adjustment_list'),
path('stock-adjustments/create/', stock_adjustment_views.stock_adjustment_create, name='stock_adjustment_create'),
path('stock-adjustments/<int:pk>/', stock_adjustment_views.stock_adjustment_detail, name='stock_adjustment_detail'),
```

### 6. Sidebar Navigation
Updated the sidebar to include a new menu item:
- **Lost/Damaged Items** - Under the Supplies dropdown menu
- Icon: `fa-tools`
- Access restricted to admin and GSO staff

## Database Migration
Migration `0020_alter_inventorytransaction_transaction_type.py` was created and applied to add the new transaction types.

## Usage

### Recording an Adjustment
1. Navigate to **Supplies > Lost/Damaged Items**
2. Click **Record Adjustment** button
3. Select the adjustment type (Lost or Damaged)
4. Choose the affected supply item
5. Enter the quantity affected
6. Provide details about what happened
7. Click **Record Adjustment**

### Viewing Adjustments
1. Navigate to **Supplies > Lost/Damaged Items**
2. View the table of all adjustments
3. Use filters to narrow results:
   - By supply item
   - By type (Lost/Damaged)
   - By search term

### Viewing Details
1. Click the **View** button next to any adjustment
2. See complete details including:
   - Item affected
   - Stock impact
   - Loss value
   - Who recorded it
   - When it was recorded
   - Reason/description

## Permissions
- **Admin**: Full access
- **GSO Staff**: Full access
- **Department Users**: No access

## Data Validation
- Quantity must be positive (minimum 1)
- Cannot adjust more items than currently in stock
- Description is required
- Supply selection is required

## Audit Trail
- All adjustments create an `InventoryTransaction` record
- Tracks who made the adjustment
- Records when the adjustment was made
- Stores the quantity changed and impact on stock
- Preserves the reason/description

## Statistics
The list view displays:
- **Total Adjustments**: All lost and damaged records
- **Lost Items**: Sum of all items marked as lost
- **Damaged Items**: Sum of all items marked as damaged

## Integration
- Integrates with existing supply management system
- Uses existing `InventoryTransaction` model for audit trail
- Works with existing supply filtering and search
- Follows existing design patterns and UI conventions

## Benefits
1. **Accountability**: Tracks who recorded each adjustment and when
2. **Traceability**: Complete history of lost/damaged items
3. **Accuracy**: Maintains inventory accuracy automatically
4. **Analysis**: Can identify problem items or frequent losses
5. **Reporting**: Data available for inventory reports
