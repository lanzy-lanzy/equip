# Available Quantity Display Feature

## Overview
When department users submit a borrow request, they now see the available quantity of each item in real-time as they select from the dropdown. This helps them make informed decisions about how much to borrow.

## Changes Made

### 1. **Updated Form Display** (forms.py)
- Enhanced `BorrowRequestForm` to show available quantity in dropdown labels
- Example: "Wireless Mouse (8 pieces available)"
- Users can see at a glance how much is available

### 2. **Template Enhancement** (request_borrow_item.html)
- Added "Available Quantity" info box that appears when an item is selected
- Shows:
  - Available quantity
  - Unit type (pieces, units, etc.)
  - "You can borrow up to this amount" helpful text
- Box is hidden until an item is selected

### 3. **JavaScript Enhancement**
- Created `supplies_data` JSON object passed from view to template
- JavaScript listens to supply selection changes
- Updates available quantity display in real-time
- Validates that requested quantity doesn't exceed available amount
- Auto-adjusts max quantity on quantity input field

### 4. **View Enhancement** (views.py)
- Updated `request_borrow_item` view to pass supply data to template
- Generates JSON object with supplies' quantity and unit information
- Only shows supplies with available stock (quantity > 0)

## User Flow

1. User navigates to "Borrow Item" page
2. User clicks on "Select Item to Borrow" dropdown
3. Sees list of available items with quantities in parentheses:
   - "Wireless Mouse (8 pieces available)"
   - "Laptop Stand (3 items available)"
4. User selects an item
5. "Available Quantity" info box appears below dropdown showing:
   - Available: 8 pieces
   - You can borrow up to this amount
6. User enters quantity (max = available quantity)
7. User can't enter more than available

## Technical Details

### Data Flow
```
View (request_borrow_item)
  ↓
supplies = Supply.objects.filter(quantity__gt=0)
form.fields['supply'].queryset = supplies
supplies_data = JSON array: [
  {id: 1, quantity: 8, unit: "pieces"},
  {id: 2, quantity: 3, unit: "items"},
  ...
]
  ↓
Template receives supplies_data
  ↓
JavaScript parses supplies_data into suppliesMap
  ↓
On select change: JavaScript updates available info box
```

### JavaScript Map Structure
```javascript
suppliesMap = {
  1: {id: 1, quantity: 8, unit: "pieces"},
  2: {id: 2, quantity: 3, unit: "items"},
  ...
}
```

## Visual Example

### Before Selection
```
Select Item to Borrow *
[Choose an item...]
Choose the item you want to borrow
```

### After Selection
```
Select Item to Borrow *
[Wireless Mouse (8 pieces available)]
Choose the item you want to borrow

✓ Available: 8 pieces
  You can borrow up to this amount
```

## Validation

- If user selects an item and then manually changes quantity to exceed available, the form still validates on the server side
- JavaScript helps prevent invalid input by setting max on quantity input
- Form backend also validates during submission

## Benefits

1. **Clear Information**: Users see exactly how much is available
2. **Better UX**: No surprises about available quantities
3. **Prevents Overages**: Max quantity is enforced on input
4. **Shows Units**: Different items can have different units (pieces, items, etc.)
5. **Real-Time Updates**: Changes instantly when user selects different item

## Testing

1. Navigate to "Borrow Item" as a department user
2. Click the supply dropdown
3. Note that all items show available quantity in parentheses
4. Select an item
5. Verify that the "Available Quantity" box appears
6. Try entering a quantity greater than available - should be limited by input max
7. Submit the form - should work with valid quantity

## No Database Changes

This feature requires no database migration. All data comes from existing Supply model fields:
- `supply.name`
- `supply.quantity`
- `supply.unit`
