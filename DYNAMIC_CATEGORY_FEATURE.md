# Dynamic Category Creation Feature

## Overview
The Supply Management System now includes the ability to create supply categories dynamically during supply item creation. This eliminates the need to pre-populate all categories and allows GSO staff to add new categories on-the-fly when creating supplies.

## Features

### 1. Category Creation UI
- **"Add" button** on the Category field in the supply creation form
- Clicking the button reveals a category creation section with input field
- Users can enter a new category name or cancel the operation

### 2. Automatic Category Management
- When creating a supply with a new category, the category is automatically created and assigned
- If the category already exists (case-insensitive check), it will be reused
- Categories are persisted in the database for future use

### 3. Consumable vs Non-Consumable Support
The form continues to support the distinction between:
- **Non-Consumable (Equipment)**: Reusable items like printers, mice, keyboards
- **Consumable (Supplies)**: Disposable items like paper, pens, ink

## How to Use

### Creating a Supply with Existing Category
1. Go to **Supplies > Add New Supply** (or the Create Supply page)
2. Fill in the supply name
3. Click on the **Category** dropdown and select from existing categories
4. Select the supply type (Consumable or Non-Consumable)
5. Fill in other required fields (description, quantity, etc.)
6. Click **Create Supply**

### Creating a Supply with New Category
1. Go to **Supplies > Add New Supply**
2. Fill in the supply name
3. Click the **"+ Add"** button next to the Category field
4. A category creation section will appear
5. Enter the new category name (e.g., "Electronics", "Office Supplies")
6. Click **"Create Category"** or press Enter
7. The new category will be automatically selected
8. Select the supply type (Consumable or Non-Consumable)
9. Fill in other required fields
10. Click **Create Supply**

## Technical Implementation

### Backend Changes

#### Forms (inventory/forms.py)
- Added `new_category` field to `SupplyForm`
- Enhanced validation to accept either an existing category or a new category name
- Modified `save()` method to create category if new_category is provided

#### Views (inventory/views.py)
- Added `create_category_api()` endpoint for API-based category creation
- Validates category name length and uniqueness
- Returns JSON response with created category details

#### URLs (inventory/urls.py)
- Added route: `api/categories/create/` → `create_category_api`

### Frontend Changes

#### Template (templates/inventory/supply_form.html)
- Added "Add" button next to Category dropdown
- Added hidden category creation section with:
  - Category name input field
  - Create and Cancel buttons
  - Help tip for users
- Added JavaScript event handlers for:
  - Showing/hiding category creation section
  - Validating category name
  - Checking for duplicates
  - Adding new category to dropdown
  - Keyboard support (Enter to create)

## Validation Rules

### Category Name Validation
- Minimum 2 characters required
- Cannot be empty
- Case-insensitive duplicate checking
- Maximum 100 characters (database field limit)

### Form Validation
- User must select either:
  - An existing category from the dropdown, OR
  - Enter a new category name to create
- Cannot leave category field blank without providing a new category name

## Database Impact

### SupplyCategory Model
No changes to the model structure. The feature uses the existing `SupplyCategory` model:
```python
class SupplyCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
```

## Permissions

- **GSO Staff**: Can create supplies with new categories
- **Admins**: Can create supplies with new categories
- **Department Users**: Cannot access supply creation

## Error Handling

### Client-Side Validation
- Alert if category name is empty
- Alert if category name is less than 2 characters
- Alert if category already exists in dropdown
- Success message when category is created (auto-disappears after 3 seconds)

### Server-Side Validation
- Validates category name length
- Checks for duplicate categories (case-insensitive)
- Returns appropriate error messages

## User Experience Enhancements

### Visual Feedback
- Success message appears when category is created
- Auto-focus on category name input when creation section opens
- Smooth hide/show animations

### Keyboard Support
- Press **Enter** to create category from the input field
- Standard form navigation with Tab key

### Responsive Design
- Works on mobile, tablet, and desktop
- Touch-friendly buttons and inputs
- Proper spacing and layout on all screen sizes

## Future Enhancements

Potential improvements for future versions:
1. Category description input during creation
2. Category icons/colors for better visual organization
3. Bulk category import/export
4. Category-based inventory reports
5. Auto-suggest categories based on supply name
6. Category search/filter in large lists

## Troubleshooting

### Category not appearing in dropdown
- Ensure you clicked "Create Category" button
- Check that the category name is unique (not already in the list)
- Verify that GSO Staff or Admin role is assigned

### Form submission fails after creating category
- Ensure the new category is selected (highlighted) in the dropdown
- Check browser console for JavaScript errors
- Verify all required fields are filled

### Duplicate category error
- The system prevents creating categories with the same name
- Try using a slightly different name or select the existing category from the list

## Integration with Existing Features

The dynamic category feature integrates seamlessly with:
- **Supply filtering** by category
- **Supply search** functionality
- **Supply requests** categorization
- **Reports and exports** that include category information
- **QR code generation** for supplies

## API Reference

### Create Category Endpoint
**Endpoint**: `POST /api/categories/create/`

**Required Parameters**:
- `name` (string): Category name (2-100 characters)

**Optional Parameters**:
- `description` (string): Category description

**Response** (Success):
```json
{
    "success": true,
    "category": {
        "id": 1,
        "name": "Electronics",
        "description": "Electronic devices and components"
    },
    "message": "Category \"Electronics\" created successfully"
}
```

**Response** (Error):
```json
{
    "success": false,
    "error": "Category with this name already exists"
}
```

**Permissions**: GSO Staff or Admin only

## Testing

### Manual Testing Checklist
- [ ] Create supply with existing category
- [ ] Create supply with new category
- [ ] Verify new category appears in dropdown
- [ ] Test duplicate category prevention
- [ ] Test form validation with missing category
- [ ] Test on mobile/tablet devices
- [ ] Verify keyboard support (Enter key)
- [ ] Test with different user roles

### Data Verification
- Check database for new categories: `SELECT * FROM inventory_supplycategory;`
- Verify supply-category relationship: `SELECT * FROM inventory_supply WHERE category_id = X;`
