# Borrow Item - Non-Consumable Only Implementation

## Overview
The "Request to Borrow Item" form now shows **only non-consumable items (equipment)**, making it clear that this form is exclusively for borrowing reusable equipment rather than requesting consumable supplies.

## Changes Made

### 1. **Form Update** (`BorrowRequestForm` in `inventory/forms.py`)
Changed from showing grouped choices to showing **only non-consumable items**:

```python
def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    # Filter supplies - only NON-CONSUMABLE items (equipment) with available stock
    supply_field = self.fields['supply']
    supply_field.queryset = Supply.objects.filter(quantity__gt=0, is_consumable=False).order_by('name')
    
    # Build choices with quantity info
    choices = [('', '-- Select equipment to borrow --')]
    for supply in supply_field.queryset:
        label = f"{supply.name} ({supply.quantity} {supply.unit} available)"
        choices.append((supply.pk, label))
    
    supply_field.choices = choices
```

**Before:** Showed both consumable and non-consumable items in grouped optiongroups
**After:** Shows only non-consumable items (equipment)

### 2. **Template Update** (`request_borrow_item.html`)

#### Removed Consumable Section
- Removed the entire "Consumable Items (Supplies)" section
- Removed the JavaScript logic that rendered consumable items

#### Updated Supply Selection
- Added blue info box explaining this form is for equipment only
- Shows emoji and clear messaging about non-consumable items
- Displays examples (printers, keyboards, monitors)

```html
<!-- Non-Consumable Items Section (Equipment Only) -->
<div class="bg-blue-50 border-2 border-blue-200 rounded-lg p-4 mb-4">
    <p class="text-sm font-medium text-blue-900 mb-3">
        <i class="fas fa-cube text-blue-600 mr-2"></i>📦 Equipment Items Only
    </p>
    <p class="text-sm text-blue-700 mb-3">
        This form is for borrowing <strong>non-consumable equipment</strong> 
        (items you can reuse like printers, keyboards, monitors, etc.)
    </p>
</div>
```

### 3. **View Update** (`request_borrow_item` in `inventory/views.py`)
Simplified to provide only non-consumable supplies to the template:

```python
# Prepare supplies data for the template - only non-consumable items
non_consumable_supplies = [
    {
        'id': s.pk,
        'name': s.name,
        'quantity': s.quantity,
        'unit': s.unit or 'pieces',
        'is_consumable': False
    }
    for s in Supply.objects.filter(quantity__gt=0, is_consumable=False).order_by('name')
]

context = {
    'form': form,
    'non_consumable_supplies': json.dumps(non_consumable_supplies),
}
```

**Before:** Prepared both consumable and non-consumable supplies
**After:** Only prepares non-consumable supplies

### 4. **JavaScript Update** (in `request_borrow_item.html`)
Simplified to work with only non-consumable items:

```javascript
// Parse supplies data from Django context - only non-consumable items
const nonConsumableSupplies = {{ non_consumable_supplies|safe }};

// Create a map of all supplies for quick lookup
const suppliesMap = {};
nonConsumableSupplies.forEach(supply => {
    suppliesMap[supply.id] = supply;
});

// Render non-consumable items (equipment only)
if (nonConsumableSupplies.length > 0) {
    nonConsumableContainer.innerHTML = nonConsumableSupplies.map(supply => `
        <label class="flex items-center p-3 border border-gray-300 rounded-lg hover:bg-blue-50 cursor-pointer transition-colors">
            <input type="radio" name="supply-option" value="${supply.id}" class="supply-radio w-4 h-4 text-blue-600">
            <div class="ml-3 flex-1">
                <p class="text-sm font-medium text-gray-900">${supply.name}</p>
                <p class="text-xs text-gray-500">Available: ${supply.quantity} ${supply.unit}</p>
            </div>
        </label>
    `).join('');
} else {
    nonConsumableContainer.innerHTML = '<p class="text-sm text-gray-500 italic">No equipment items available for borrowing</p>';
}
```

**Before:** Rendered both consumable and non-consumable in separate sections
**After:** Only renders non-consumable equipment

## User Experience

### What Users See
1. Clear messaging that this form is **only for borrowing equipment**
2. Blue info box with examples of equipment items
3. Only equipment items appear in the selection list
4. No confusing consumable items in the dropdown

### Example Equipment Display
```
Select Item to Borrow
├── 📦 Equipment Items Only
├── Printer HP LaserJet (5 pieces available)
├── Keyboard USB (12 pieces available)
├── Monitor 24" (3 pieces available)
└── Mouse Logitech (10 pieces available)
```

## Clear Separation Between Forms

### Create Request (Consumable Supplies)
- For: Paper, pens, ink, highlighters, etc.
- Action: Item is issued immediately when approved
- Tracking: Not tracked with return deadline

### Request for Equipment (Non-Consumable Items)
- For: Printers, keyboards, monitors, etc.
- Action: GSO staff approves and sets return deadline
- Tracking: Tracked with exact return date
- Duration: User specifies borrowing duration (default 3 days)

## Files Modified

1. **inventory/forms.py**
   - Updated `BorrowRequestForm.__init__()` to filter only non-consumable items

2. **templates/inventory/request_borrow_item.html**
   - Removed consumable items section
   - Added equipment-only info box
   - Simplified JavaScript logic

3. **inventory/views.py**
   - Updated `request_borrow_item()` view to prepare only non-consumable supplies

## Testing Checklist

- [ ] "Request to Borrow Item" dropdown shows only non-consumable items
- [ ] No consumable items appear in the dropdown
- [ ] Info box explains equipment-only borrowing
- [ ] Radio buttons work correctly
- [ ] Selected item information displays properly
- [ ] Quantity validation works
- [ ] Duration field appears and works
- [ ] Form submits successfully
- [ ] Borrow request is created correctly
- [ ] GSO staff can approve with dates

## Benefits

1. **Clear Intent** - Users know exactly what this form is for
2. **Reduced Confusion** - No mixing of consumables and equipment
3. **Proper Workflow** - Equipment borrowing follows appropriate approval/return process
4. **Better UI** - Cleaner interface with only relevant items
5. **Simplified Code** - Less complex JavaScript and form logic
