# Supply Request Organization by Type

## Overview
The supply request form now organizes supplies by consumable and non-consumable items, making it easier for users to find and request the correct type of supply.

## Changes Implemented

### 1. **Form Enhancement** (`inventory/forms.py`)
Updated `SupplyRequestForm` to organize supplies into grouped choices:

```python
# Organize supplies by consumable/non-consumable
consumable_choices = []
non_consumable_choices = []

for supply in supply_field.queryset:
    label = f"{supply.name} ({supply.quantity} {supply.unit} available)"
    choice = (supply.pk, label)
    
    if supply.is_consumable:
        consumable_choices.append(choice)
    else:
        non_consumable_choices.append(choice)

# Create grouped choices (non-consumable items first, then consumable)
grouped_choices = []
if non_consumable_choices:
    grouped_choices.append(('📦 Non-Consumable (Equipment) - Reusable', non_consumable_choices))
if consumable_choices:
    grouped_choices.append(('💧 Consumable (Supplies) - Disposable', consumable_choices))

supply_field.choices = grouped_choices
```

### 2. **Template Enhancement** (`templates/inventory/request_form.html`)

#### A. Information Box
Added a helpful blue information box explaining the supply type organization:
```html
<div class="bg-blue-50 border-2 border-blue-200 rounded-lg p-4 mb-3">
    <p class="text-sm font-medium text-blue-900 mb-2">
        <i class="fas fa-info-circle mr-2"></i>Supplies are organized by type:
    </p>
    <ul class="text-sm text-blue-800 space-y-1">
        <li><span class="font-medium">📦 Non-Consumable:</span> Equipment you can reuse (printers, keyboards, etc.)</li>
        <li><span class="font-medium">💧 Consumable:</span> Supplies you use up (paper, pens, ink, etc.)</li>
    </ul>
</div>
```

#### B. Supply Information Display
Enhanced the supply information section to show:
- Supply Type (with emoji and description)
- Color-coded backgrounds based on supply type
  - **Blue**: Non-Consumable (Equipment)
  - **Slate/Gray**: Consumable (Supplies)
- Dynamic icons that change based on type

```html
<div id="supply-info" class="hidden p-4 rounded-lg border-2" 
     style="border-color: var(--supply-type-color); background-color: var(--supply-type-bg);">
    <h3 class="text-sm font-medium text-gray-700 mb-3">
        <i id="supply-type-icon" class="mr-2"></i>
        <span id="supply-type-label">Supply Information</span>
    </h3>
    <!-- Displays name, type, category, available stock, and unit -->
</div>
```

### 3. **JavaScript Enhancement**
Updated the form script to:

1. **Store supply type data**:
   ```javascript
   supplyData[{{ supply.id }}] = {
       name: '{{ supply.name }}',
       category: '{{ supply.category.name }}',
       stock: {{ supply.quantity }},
       unit: '{{ supply.unit }}',
       minStock: {{ supply.min_stock_level }},
       isConsumable: {{ supply.is_consumable|lower }},
       supplyType: '{{ "Consumable (Disposable)" if supply.is_consumable else "Non-Consumable (Equipment)" }}'
   };
   ```

2. **Dynamic styling based on type**:
   ```javascript
   const isConsumable = supply.isConsumable;
   const typeIcon = isConsumable ? 'fas fa-droplet' : 'fas fa-cube';
   const typeBorderColor = isConsumable ? '#94a3b8' : '#3b82f6'; // slate vs blue
   
   supplyInfo.style.setProperty('--supply-type-color', typeBorderColor);
   supplyInfo.style.setProperty('--supply-type-bg', typeBgColor);
   ```

3. **Display supply type information**:
   - Shows type with appropriate emoji (💧 or 📦)
   - Updates the information box styling
   - Shows green-colored available stock

## User Experience Improvements

### Dropdown Organization
```
Select Supply
├── 📦 Non-Consumable (Equipment) - Reusable
│   ├── Printer HP LaserJet (5 pieces available)
│   ├── Keyboard USB (12 pieces available)
│   └── Monitor 24" (3 pieces available)
│
└── 💧 Consumable (Supplies) - Disposable
    ├── A4 Paper (100 reams available)
    ├── Ballpoint Pens (500 pieces available)
    └── Ink Cartridge (25 pieces available)
```

### Visual Feedback
When a user selects a supply:
- **Non-Consumable items** → Blue-bordered information box with cube icon
- **Consumable items** → Slate/gray-bordered information box with droplet icon
- Shows all relevant details with color-coded available stock

## Benefits

1. **Improved Organization**: Users can quickly find supplies by category
2. **Clear Differentiation**: Visual cues (colors, icons, emojis) help users understand supply types
3. **Better UX**: Information box explains the difference between types
4. **Stock Visibility**: Available quantity is highlighted in green
5. **Type Awareness**: Helps users understand what they're requesting (reusable vs. consumable)

## Testing Checklist

- [ ] Non-consumable items appear in first group
- [ ] Consumable items appear in second group
- [ ] Only supplies with available stock are shown
- [ ] Selecting a supply displays type-specific styling
- [ ] Supply information updates correctly
- [ ] Color changes based on supply type (blue vs slate)
- [ ] Icons change based on supply type
- [ ] Quantity validation works correctly
- [ ] Form submits successfully with organized supplies
