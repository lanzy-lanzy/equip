# Request Types Separation

## Overview
The supply request system now separates consumable and non-consumable items into two distinct request types:

1. **Create Request** - For consumable supplies (what you use up)
2. **Request for Equipment** - For borrowing non-consumable items (what you reuse)

## Changes Made

### 1. Supply Request Form (`SupplyRequestForm`)
Modified to show **ONLY consumable items**:

```python
# Filter supplies - only CONSUMABLE items with available stock
supply_field.queryset = Supply.objects.filter(quantity__gt=0, is_consumable=True).order_by('name')
```

**Before:** Showed all supplies mixed together
**After:** Only shows consumable supplies (paper, pens, ink, etc.)

### 2. Template Updates (`request_form.html`)

#### Information Box
Added clear messaging that this form is for consumable items only:
- Explains what consumable supplies are
- Provides link to "Request for Equipment" form for borrowing
- Shows icons and descriptions of both types

#### Supply Information Display
- Simplified to show only relevant info (no type switching needed)
- Always shows slate/gray theme (consumable style)
- Displays name, category, available stock, and unit

### 3. JavaScript Simplification
- Removed dynamic type detection
- All supplies are consumable, so no need for conditional styling
- Cleaner, more maintainable code

## User Flow

### For Consumable Supplies (Paper, Pens, Ink, etc.)
1. User clicks "New Request" 
2. Selects from consumable items only
3. Enters quantity and purpose
4. Submits - item is issued immediately when approved

### For Non-Consumable Items (Printers, Keyboards, Monitors, etc.)
1. User clicks "Request for Equipment"
2. Selects from equipment items only  
3. Enters borrow duration (default 3 days)
4. Submits - GSO staff approves and sets exact return date
5. Item is tracked with return deadline

## Benefits

1. **Clear Separation** - Users know exactly which form to use
2. **Simplified Logic** - Each form handles one type consistently
3. **Better UX** - No confusion about supply types
4. **Proper Workflow** - Consumables vs. borrowables follow their own processes
5. **Easier Tracking** - System tracks consumables and equipment differently

## Dropdown Display

### Create Request (Consumable Items)
```
Select Consumable Supply
├── A4 Paper (100 reams available)
├── Ballpoint Pens (500 pieces available)
├── Ink Cartridge (25 pieces available)
└── Highlighters (80 pieces available)
```

### Request for Equipment (Non-Consumable Items)
```
Select Equipment Item
├── Printer HP LaserJet (5 pieces available)
├── Keyboard USB (12 pieces available)
├── Monitor 24" (3 pieces available)
└── Mouse Logitech (10 pieces available)
```

## Related Files Modified

1. `inventory/forms.py`
   - Updated `SupplyRequestForm.__init__()` to filter consumable items

2. `templates/inventory/request_form.html`
   - Updated info box messaging
   - Simplified supply information display
   - Simplified JavaScript logic

3. `templates/inventory/request_borrow_item.html`
   - Already shows non-consumable items only (no changes needed)

## Testing Checklist

- [ ] Create Request dropdown shows only consumable items
- [ ] Request for Equipment dropdown shows only non-consumable items  
- [ ] No consumable items appear in Equipment request
- [ ] No non-consumable items appear in regular request
- [ ] Supply information displays correctly
- [ ] Quantity validation works
- [ ] Form submits successfully
- [ ] Link to "Request for Equipment" works from regular request form
