# Consumable vs Non-Consumable Items Separation

## Overview
This feature separates consumable and non-consumable items in the "Request to Borrow Item" form, allowing users to quickly identify and select the type of item they need to borrow.

## Changes Made

### 1. Database Model Changes
**File: `inventory/models.py`**
- Added `is_consumable` field to the `Supply` model:
  - Type: `BooleanField`
  - Default: `False` (items are non-consumable by default)
  - Help text: "Check if this item is consumable (e.g., paper, pens). Unchecked means non-consumable (e.g., equipment)"

### 2. Database Migration
**File: `inventory/migrations/0008_supply_is_consumable.py`**
- New migration that adds the `is_consumable` field to the Supply table
- Run with: `python manage.py migrate`

### 3. Form Updates
**File: `inventory/forms.py`**

#### SupplyForm
- Added `is_consumable` field to the form
- Added checkbox widget for easy toggling

#### BorrowRequestForm
- Modified to group supplies by consumable type
- Creates grouped choices:
  - "Non-Consumable Items" group
  - "Consumable Items" group
- Displays available quantity with each item

### 4. View Updates
**File: `inventory/views.py`**

#### request_borrow_item view
- Separated supplies into two lists:
  - `consumable_supplies`: Items marked as consumable
  - `non_consumable_supplies`: Items marked as non-consumable
- Passes both lists to template as JSON for frontend rendering

### 5. Template Updates
**File: `templates/inventory/request_borrow_item.html`**

#### UI Changes:
- **Non-Consumable Items Section**
  - Icon: Box icon (fa-box) in blue
  - Label: "Non-Consumable Items (Equipment)"
  - Display: Radio buttons with supply name and available quantity

- **Consumable Items Section**
  - Icon: Droplet icon (fa-droplet) in green
  - Label: "Consumable Items (Supplies)"
  - Display: Radio buttons with supply name and available quantity

- **Selected Item Display**
  - Shows the selected item name
  - Shows item type (Consumable vs Non-Consumable)
  - Shows available quantity and unit
  - Updates in real-time as user selects different items

#### JavaScript Enhancements:
- Renders items from JSON data (no select dropdown required)
- Radio button selection interface instead of select dropdown
- Real-time updating of selected item information
- Validation of quantity input against available stock
- Color-coded sections (blue for equipment, green for supplies)

## Setup Instructions

### 1. Apply Database Migration
```bash
python manage.py migrate
```

### 2. Classify Existing Items (Optional)
The system provides a helper script to automatically classify items based on keywords:

```bash
python manage.py shell < setup_consumable_types.py
```

This script will:
- Scan all supplies
- Check names and descriptions for consumable keywords
- Automatically mark items appropriately
- Display results

### 3. Manual Classification
You can also manually classify items:
1. Go to Admin panel (`/admin`)
2. Select "Supplies"
3. Edit each supply
4. Check/uncheck "Is Consumable" checkbox
5. Save

## Consumable vs Non-Consumable Definition

### Consumable Items (is_consumable = True)
Items that are used up and need to be replenished:
- Paper, pens, pencils
- Printer toner/ink
- Staples, clips
- Sticky notes
- Cleaners, disinfectants
- Other disposable supplies

### Non-Consumable Items (is_consumable = False)
Items that can be returned and reused:
- Equipment (printers, scanners)
- Computers, keyboards, mice
- Furniture
- USB drives
- Cables and adapters
- Tools and instruments

## User Interface

### Before Selection
```
Non-Consumable Items (Equipment)
[☐] USB Flash Drive 32GB (24 pieces available)
[☐] Wireless Mouse (15 pieces available)
[☐] Keyboard (5 pieces available)

Consumable Items (Supplies)
[☐] A4 Printer Paper (0 reams available)
[☐] Ballpen Black (63 pieces available)
[☐] Disinfectant Spray (4 bottles available)
[☐] Floor Wax (1 gallons available)
```

### After Selection
```
Selected Item:
USB Flash Drive 32GB
(Equipment - Non-Consumable)

Available: 24 pieces
```

## API/Data Structure

### consumable_supplies JSON
```json
[
  {
    "id": 1,
    "name": "Ballpen Black",
    "quantity": 63,
    "unit": "pieces",
    "is_consumable": true
  }
]
```

### non_consumable_supplies JSON
```json
[
  {
    "id": 5,
    "name": "USB Flash Drive 32GB",
    "quantity": 24,
    "unit": "pieces",
    "is_consumable": false
  }
]
```

## Features

✅ Clear visual separation between item types
✅ Color-coded sections (blue for equipment, green for supplies)
✅ Real-time available quantity display
✅ Icon indicators for item type
✅ Radio button interface for easy selection
✅ Responsive design (works on mobile and desktop)
✅ Automatic quantity validation
✅ Empty state handling

## Testing

1. **Add supplies** via Admin panel
2. **Mark some as consumable** using the `is_consumable` checkbox
3. **Navigate to** "Request to Borrow Item" page
4. **Verify** that items are separated into two groups
5. **Select items** and verify:
   - Selected item info appears
   - Available quantity is correct
   - Item type is correctly displayed
   - Quantity input is validated against available stock

## Future Enhancements

- Filter by category in addition to consumable type
- Search functionality within each section
- Bulk item management tools
- Borrowing history per item type
- Different return policies for consumable vs non-consumable items
- Analytics dashboard showing borrowing patterns by item type
