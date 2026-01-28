# GSO Staff Template - Available Quantity Display Fix

## Issue
In the GSO staff borrow approval template (`approve_borrow_request.html`), the available quantity was not displaying the unit properly (e.g., "pieces", "items").

## Fix Applied

### Updated approve_borrow_request.html

#### 1. **Item & Available Quantity Section**
Enhanced the item display with a prominent green box showing available stock:

**Before:**
```html
<div>
    <label class="text-sm font-medium text-gray-700">Item</label>
    <p class="text-gray-900">{{ supply_request.supply.name }}</p>
    <p class="text-sm text-gray-600">Available: {{ supply_request.supply.quantity }} {{ supply_request.supply.unit }}</p>
</div>
```

**After:**
```html
<div>
    <label class="text-sm font-medium text-gray-700">Item</label>
    <p class="text-gray-900 font-medium">{{ supply_request.supply.name }}</p>
    <div class="mt-2 p-2 bg-green-50 border border-green-200 rounded">
        <p class="text-sm font-medium text-green-900">
            <i class="fas fa-check-circle text-green-600 mr-1"></i>
            Available: <span class="font-bold text-green-700">{{ supply_request.supply.quantity }}</span> 
            <span class="font-medium text-green-700">{{ supply_request.supply.unit|default:"pieces" }}</span>
        </p>
    </div>
</div>
```

#### 2. **Quantity Requested Section**
Improved visibility and unit display:

**Before:**
```html
<div>
    <label class="text-sm font-medium text-gray-700">Quantity Requested</label>
    <p class="text-gray-900">{{ supply_request.quantity_requested }} {{ supply_request.supply.unit }}</p>
</div>
```

**After:**
```html
<div>
    <label class="text-sm font-medium text-gray-700">Quantity Requested</label>
    <p class="text-gray-900 text-lg font-semibold">
        {{ supply_request.quantity_requested }} 
        <span class="text-sm font-normal text-gray-600">{{ supply_request.supply.unit|default:"pieces" }}</span>
    </p>
</div>
```

## Key Improvements

1. **Green Status Box** - Available quantity now displays in a green info box, making it prominent and easy to see
2. **Icon & Styling** - Added checkmark icon for visual emphasis
3. **Unit Filter** - Used Django's `|default:"pieces"` filter to ensure unit always displays
4. **Better Contrast** - Bold quantity with regular unit text for clear hierarchy
5. **Mobile Friendly** - Responsive layout maintained

## Visual Result

### Item Section
```
Item
Wireless Mouse

✓ Available: 8 pieces
```

### Quantity Requested Section
```
Quantity Requested
5 pieces
```

## Benefits for GSO Staff

- **Clear Stock Check**: Immediately see how much is available before approval
- **Better Decision Making**: Know if the requested quantity is appropriate
- **Professional Display**: Clean, organized information layout
- **Consistent UI**: Matches other quantity displays throughout the app

## Testing Steps

1. Go to Requests → Find a pending borrow request
2. Click Approve
3. You should see the GSO approval page
4. Check that the "Available" section shows:
   - Green box with checkmark icon
   - Number in bold
   - Unit type clearly visible (pieces, items, etc.)
5. Verify "Quantity Requested" also shows unit properly

## No Database Changes Required

This is purely a template display fix. No database migrations or backend changes needed.
