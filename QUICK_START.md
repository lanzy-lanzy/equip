# Quick Start: Consumable vs Non-Consumable Items

## 3-Step Setup

### Step 1: Apply Database Migration
```bash
python manage.py migrate
```

### Step 2: Classify Your Items
Choose one approach:

**Option A - Automatic Classification (Recommended)**
```bash
python manage.py shell < setup_consumable_types.py
```
This automatically marks items based on keywords.

**Option B - Manual Classification**
1. Go to Django Admin: `/admin`
2. Click on "Supplies"
3. For each item, check "Is Consumable" if it's a disposable supply
4. Save

### Step 3: Test
1. Go to "Request to Borrow Item" page
2. You should see two sections:
   - **Non-Consumable Items (Equipment)** - with 📦 icon
   - **Consumable Items (Supplies)** - with 💧 icon
3. Try selecting items from each section
4. Verify the selected item info updates correctly

## What Changed?

### Supply Model
- Added `is_consumable` checkbox field
- Default: unchecked (treats items as non-consumable equipment)

### Borrow Request Form
- Old: Single dropdown with all items mixed
- New: Separated into two clear sections with radio buttons

### Visual Design
- **Equipment Section** (Blue, 📦 icon)
  - USB drives, mice, keyboards, printers, etc.
  - For items that are returned and reused

- **Supplies Section** (Green, 💧 icon)
  - Paper, pens, ink, cleaning supplies, etc.
  - For consumable/disposable items

## Item Classification Rules

**Consumable = TRUE** if item is:
- Disposed after use
- Used up/consumed
- Requires regular replenishment
- Single-use or wear-out items

**Consumable = FALSE** (Equipment) if item is:
- Reusable equipment
- Returned after borrowing
- Durable goods
- Infrastructure items

## Admin Configuration

### In Django Admin:
1. Go to `/admin`
2. Select "Supplies"
3. Edit each supply record
4. Toggle "Is Consumable" checkbox:
   - ✓ Checked = Consumable (supplies)
   - ☐ Unchecked = Equipment (non-consumable)
5. Click "Save"

## Examples

### Items to Mark as CONSUMABLE (✓)
- A4 Printer Paper
- Ballpens
- Ink Cartridges
- Staples
- Sticky Notes
- Disinfectant Spray
- Floor Wax
- Tissue Paper
- Erasers

### Items to Mark as NON-CONSUMABLE (☐)
- USB Flash Drives
- Wireless Mouse
- Keyboard
- Printers
- Scanners
- Computers
- Cables
- Adapters
- Furniture

## Features

✅ Clear visual separation
✅ Color-coded sections
✅ Icons for quick identification
✅ Real-time availability display
✅ Easy radio button selection
✅ Mobile responsive
✅ Works with existing borrowing system

## Troubleshooting

**Problem:** "No non-consumable items available" message
- **Solution:** Make sure you have items marked as non-consumable (☐) in Admin

**Problem:** "No consumable items available" message
- **Solution:** Make sure you have items marked as consumable (✓) in Admin

**Problem:** Items not appearing in sections
- **Solution:** Check that items have quantity > 0

**Problem:** Migration fails
- **Solution:** Ensure you're in the correct directory and Django is installed

## Files Modified

- `inventory/models.py` - Added is_consumable field
- `inventory/forms.py` - Added field to forms
- `inventory/views.py` - Updated view logic
- `templates/inventory/request_borrow_item.html` - New UI
- `inventory/migrations/0008_supply_is_consumable.py` - Database change

## Documentation

- Full documentation: `CONSUMABLE_NONCONSUMABLE_SEPARATION.md`
- Implementation details: `IMPLEMENTATION_SUMMARY.txt`

---

**Ready to test?** Go to the "Request to Borrow Item" page and you should see the new interface!
