# Dynamic Category Creation - Testing Checklist

## Pre-Testing Setup

- [ ] Verify Django project is running: `python manage.py runserver`
- [ ] Database is up to date: `python manage.py migrate`
- [ ] Logged in as GSO Staff or Admin user
- [ ] Browser developer tools open (F12) for error checking
- [ ] Have 2-3 existing categories in database (for selection testing)

---

## Unit Testing Scenarios

### 1. Form Functionality Tests

#### Test 1.1: Form Loads Correctly
- [ ] Navigate to `/supplies/create/`
- [ ] Verify form displays all fields:
  - [ ] Supply Name input
  - [ ] Category dropdown with existing categories
  - [ ] [+Add] button visible next to Category
  - [ ] Supply Type radio buttons (Non-Consumable, Consumable)
  - [ ] Description textarea
  - [ ] Quantity, Min Stock Level, Unit inputs
  - [ ] Cost per Unit input
  - [ ] Location input
  - [ ] [Create Supply] and [Cancel] buttons

#### Test 1.2: Category Dropdown Shows Options
- [ ] Dropdown contains all existing categories
- [ ] Categories listed in alphabetical order
- [ ] Default option shows "--------"
- [ ] Can select each category from dropdown

#### Test 1.3: Category Creation Section Hidden by Default
- [ ] Category creation section NOT visible when page loads
- [ ] Section is hidden with CSS class `hidden`
- [ ] No focus on category input field initially

---

### 2. UI Interaction Tests

#### Test 2.1: Show Category Creation Section
- [ ] Click [+Add] button
- [ ] Category creation section reveals with smooth animation
- [ ] Input field gets focus (cursor visible)
- [ ] Cancel and Create buttons are clickable
- [ ] Text shows "Create New Category" header

#### Test 2.2: Hide Category Creation Section
- [ ] Click [Cancel] button
- [ ] Category creation section hides smoothly
- [ ] Input field cleared
- [ ] Focus returns to normal

#### Test 2.3: Cancel via Outside Click (if implemented)
- [ ] Click outside category creation section (TBD implementation)
- [ ] Section hides

---

### 3. Input Validation Tests (Client-Side)

#### Test 3.1: Empty Category Name
- [ ] Click [+Add]
- [ ] Leave input empty
- [ ] Click [Create Category]
- [ ] Alert shows: "Please enter a category name"
- [ ] Form doesn't proceed

#### Test 3.2: Too Short Category Name
- [ ] Click [+Add]
- [ ] Enter single character: "A"
- [ ] Click [Create Category]
- [ ] Alert shows: "Category name must be at least 2 characters long"
- [ ] Section remains open

#### Test 3.3: Valid Category Name
- [ ] Click [+Add]
- [ ] Enter 2+ character name: "Electronics"
- [ ] Click [Create Category]
- [ ] No alert shown
- [ ] Category added to dropdown

#### Test 3.4: Duplicate Prevention (Client)
- [ ] Click [+Add]
- [ ] Select a category from dropdown: "Office Supplies"
- [ ] Type same name: "Office Supplies"
- [ ] Click [Create Category]
- [ ] Alert shows: "This category already exists"
- [ ] Category not re-added to dropdown

---

### 4. Dropdown Manipulation Tests

#### Test 4.1: New Category Added to Dropdown
- [ ] Click [+Add]
- [ ] Enter new category: "Furniture"
- [ ] Click [Create Category]
- [ ] New option appears in Category dropdown
- [ ] New category is pre-selected (highlighted)
- [ ] Success message appears: "✓ Category 'Furniture' created and selected!"

#### Test 4.2: Multiple Category Creation
- [ ] Create first category: "Furniture"
- [ ] Verify it appears in dropdown
- [ ] Click [+Add] again
- [ ] Create second category: "Lighting"
- [ ] Verify both categories now in dropdown
- [ ] Both remain selectable

#### Test 4.3: Category List Order
- [ ] Create multiple categories in random order
- [ ] Verify dropdown maintains alphabetical order (or insertion order)
- [ ] Original categories still present

---

### 5. Form Submission Tests

#### Test 5.1: Submit with Existing Category
- [ ] Fill Supply Name: "Desk Lamp"
- [ ] Select Category from dropdown: "Lighting"
- [ ] Select Supply Type: "Non-Consumable"
- [ ] Fill Description: "LED desk lamp"
- [ ] Fill Quantity: 10
- [ ] Fill Min Stock Level: 2
- [ ] Fill Unit: "pieces"
- [ ] Click [Create Supply]
- [ ] Success: Supply created with selected category
- [ ] Supply list shows new item under "Lighting" category

#### Test 5.2: Submit with New Category
- [ ] Fill Supply Name: "USB Cables"
- [ ] Click [+Add] and create new category: "Connectors"
- [ ] Verify "Connectors" selected in dropdown
- [ ] Select Supply Type: "Non-Consumable"
- [ ] Fill Description: "USB Type-C cables"
- [ ] Fill Quantity: 50
- [ ] Fill Min Stock Level: 10
- [ ] Fill Unit: "pieces"
- [ ] Click [Create Supply]
- [ ] Success: Supply created, category "Connectors" created
- [ ] Supply list shows new item under "Connectors"
- [ ] "Connectors" available for future supplies

#### Test 5.3: Submit Without Category
- [ ] Fill Supply Name: "Paper Reams"
- [ ] Don't select category
- [ ] Don't create new category
- [ ] Try to click [Create Supply]
- [ ] Form shows error: "Please either select an existing category..."
- [ ] Form not submitted

#### Test 5.4: Submit with Only New Category (No Existing)
- [ ] Clear category dropdown selection if possible
- [ ] Click [+Add]
- [ ] Create new category: "Paper Products"
- [ ] Leave existing category dropdown empty (if possible)
- [ ] Fill other fields
- [ ] Click [Create Supply]
- [ ] Success: Supply created with new category

---

### 6. Keyboard Support Tests

#### Test 6.1: Tab Navigation
- [ ] Tab through form fields
- [ ] [+Add] button is reachable via Tab
- [ ] Category input field is reachable when section open
- [ ] All buttons (Create, Cancel) are reachable

#### Test 6.2: Enter Key to Create
- [ ] Click [+Add]
- [ ] Type category name: "Tools"
- [ ] Press Enter key
- [ ] Category created (not requiring mouse click)
- [ ] [Create Category] button acts same as Enter key

#### Test 6.3: Escape Key to Cancel (if implemented)
- [ ] Click [+Add]
- [ ] Press Escape key
- [ ] Category creation section hides
- [ ] Input cleared

---

### 7. Database Tests

#### Test 7.1: Category Saved to Database
- [ ] Create supply with new category: "Equipment"
- [ ] Open database: `python manage.py dbshell`
- [ ] Run: `SELECT * FROM inventory_supplycategory WHERE name='Equipment';`
- [ ] Verify: Category exists with correct name
- [ ] Verify: created_at timestamp is recent

#### Test 7.2: Supply-Category Relationship
- [ ] Create supply "Computer Mouse" with "Equipment" category
- [ ] Query: `SELECT * FROM inventory_supply WHERE name='Computer Mouse';`
- [ ] Verify: category_id matches Equipment category id

#### Test 7.3: Category Reuse
- [ ] Create supply "Keyboard" with same "Equipment" category
- [ ] Query categories: `SELECT COUNT(*) FROM inventory_supplycategory;`
- [ ] Verify: No duplicate "Equipment" category created
- [ ] Same category_id used for both supplies

#### Test 7.4: Duplicate Prevention in Database
- [ ] Try creating category "Office" via form
- [ ] Try creating category "office" (lowercase) via form
- [ ] Query: `SELECT COUNT(*) FROM inventory_supplycategory WHERE name LIKE 'Office%';`
- [ ] Verify: Only one "Office" category exists

---

### 8. API Endpoint Tests (if using AJAX version)

#### Test 8.1: POST to create_category_api
- [ ] Use curl or Postman
- [ ] POST to: `http://localhost:8000/api/categories/create/`
- [ ] Parameters: `name=NewCategory`
- [ ] Expected Response: 
  ```json
  {
    "success": true,
    "category": {
      "id": 1,
      "name": "NewCategory",
      "description": ""
    }
  }
  ```

#### Test 8.2: Duplicate Category via API
- [ ] POST same category name twice
- [ ] Second request should return error:
  ```json
  {
    "success": false,
    "error": "Category with this name already exists"
  }
  ```

#### Test 8.3: Invalid Input via API
- [ ] POST with empty name: `name=`
- [ ] Should return error: "Category name is required"
- [ ] POST with short name: `name=A`
- [ ] Should return error: "at least 2 characters"

#### Test 8.4: Authentication Required
- [ ] Log out user
- [ ] Try POST to api endpoint
- [ ] Should return 403 Forbidden or redirect to login

#### Test 8.5: Role-Based Access
- [ ] Login as Department User
- [ ] Try POST to create category
- [ ] Should return 403 Unauthorized
- [ ] Login as GSO Staff
- [ ] Try POST to create category
- [ ] Should succeed

---

### 9. Responsive Design Tests

#### Test 9.1: Desktop (1920x1080)
- [ ] [+Add] button properly positioned
- [ ] Category creation section displays correctly
- [ ] Form fields aligned properly
- [ ] No horizontal scrolling required

#### Test 9.2: Tablet (768x1024)
- [ ] Form stacks to 1 column
- [ ] [+Add] button still accessible
- [ ] Category creation section remains functional
- [ ] Touch targets are large enough

#### Test 9.3: Mobile (375x667)
- [ ] Form fully responsive
- [ ] [+Add] button clickable on small screen
- [ ] Input fields expand to fill width
- [ ] Buttons stack vertically
- [ ] Text remains readable (no overflow)

#### Test 9.4: Landscape Mobile (667x375)
- [ ] Form adapts to landscape
- [ ] No content cut off
- [ ] All controls accessible

---

### 10. Error Handling Tests

#### Test 10.1: Validation Error Messages
- [ ] Messages display clearly
- [ ] Error text in red color
- [ ] Messages don't block form
- [ ] User can correct and retry

#### Test 10.2: Server-Side Validation Errors
- [ ] Attempt to bypass client validation via browser console
- [ ] Server should still validate
- [ ] Appropriate error returned

#### Test 10.3: Database Error Handling
- [ ] Simulate database error (if possible)
- [ ] Error message displayed gracefully
- [ ] Form remains usable

#### Test 10.4: Success Messages
- [ ] Success message appears when category created
- [ ] Message displays correct category name
- [ ] Message auto-disappears after 3 seconds
- [ ] No error console output

---

### 11. Integration Tests

#### Test 11.1: Category Filtering in Supply List
- [ ] Create supply with new category via form
- [ ] Go to Supply List page
- [ ] Filter by new category
- [ ] Verify supply appears in filtered list

#### Test 11.2: Category in Supply Detail
- [ ] Create supply with new category
- [ ] Click on supply to view details
- [ ] Verify category displayed correctly

#### Test 11.3: Category in Supply Edit
- [ ] Edit existing supply
- [ ] Verify new categories available for selection
- [ ] Can change to newly-created category

#### Test 11.4: Category in Supply Requests
- [ ] Create supply with new category
- [ ] Go to Requests page
- [ ] Verify supply available for request
- [ ] Category shows in supply list

#### Test 11.5: Category in Reports
- [ ] Create supplies in multiple new categories
- [ ] Run supply report
- [ ] Verify new categories included in output
- [ ] Export CSV/PDF includes category information

---

### 12. Performance Tests

#### Test 12.1: Form Load Time
- [ ] Measure time to load supply_form page
- [ ] Should load in < 2 seconds
- [ ] Category dropdown loads with all categories

#### Test 12.2: Category Creation Speed
- [ ] Time from entering category to seeing it in dropdown
- [ ] Should be instant (< 100ms)
- [ ] No visible lag or delay

#### Test 12.3: Form Submission Time
- [ ] Create supply with new category
- [ ] Measure submission time
- [ ] Should be < 2 seconds
- [ ] Success page loads smoothly

#### Test 12.4: Large Category List
- [ ] Create 100+ categories
- [ ] Form loads without slowdown
- [ ] Dropdown still functional
- [ ] Client-side duplicate check still fast

---

### 13. Browser Compatibility Tests

#### Test 13.1: Chrome/Chromium
- [ ] Form loads correctly
- [ ] All features functional
- [ ] No console errors

#### Test 13.2: Firefox
- [ ] Form loads correctly
- [ ] All features functional
- [ ] No console errors

#### Test 13.3: Safari (if available)
- [ ] Form loads correctly
- [ ] All features functional
- [ ] No console errors

#### Test 13.4: Edge
- [ ] Form loads correctly
- [ ] All features functional
- [ ] No console errors

---

### 14. Accessibility Tests

#### Test 14.1: Keyboard Navigation
- [ ] Can reach all form fields via Tab key
- [ ] Focus indicator visible on all controls
- [ ] Logical tab order maintained

#### Test 14.2: Screen Reader (if available)
- [ ] Labels correctly associated with inputs
- [ ] Buttons have descriptive text
- [ ] Form instructions announced

#### Test 14.3: Color Contrast
- [ ] Text readable against background
- [ ] Error messages visible
- [ ] Success messages visible

#### Test 14.4: Form Labels
- [ ] All inputs have clear labels
- [ ] Required fields marked with "*"
- [ ] Help text provided where needed

---

## Automated Testing (Optional)

### Unit Tests for Form
```python
class SupplyFormTest(TestCase):
    def test_new_category_field_exists(self):
        form = SupplyForm()
        self.assertIn('new_category', form.fields)
    
    def test_clean_with_new_category(self):
        form = SupplyForm(data={
            'name': 'Test Item',
            'new_category': 'Test Category',
            'supply_type': 'False',
            'description': 'Test',
            'quantity': 10,
            'min_stock_level': 2,
            'unit': 'pieces'
        })
        self.assertTrue(form.is_valid())
    
    def test_clean_without_category(self):
        form = SupplyForm(data={
            'name': 'Test Item',
            'supply_type': 'False',
            'description': 'Test',
            'quantity': 10,
            'min_stock_level': 2,
            'unit': 'pieces'
        })
        self.assertFalse(form.is_valid())
```

### Integration Tests
```python
class SupplyCreateViewTest(TestCase):
    def test_create_supply_with_new_category(self):
        response = self.client.post('/supplies/create/', {
            'name': 'New Item',
            'new_category': 'New Category',
            'supply_type': 'False',
            'description': 'Test',
            'quantity': 10,
            'min_stock_level': 2,
            'unit': 'pieces'
        })
        self.assertEqual(response.status_code, 302)  # Redirect on success
        self.assertTrue(SupplyCategory.objects.filter(name='New Category').exists())
```

---

## Post-Testing Checklist

### Before Going to Production
- [ ] All tests passed
- [ ] No JavaScript console errors
- [ ] No Django server errors
- [ ] Database integrity verified
- [ ] Performance acceptable
- [ ] Accessibility standards met
- [ ] Documentation complete
- [ ] User training provided (if needed)

### Documentation
- [ ] README updated
- [ ] User guide provided
- [ ] Code comments added
- [ ] API documentation complete

### Monitoring
- [ ] Error logging configured
- [ ] Category creation monitored
- [ ] Form submission tracked
- [ ] Database backups enabled

---

## Test Report Template

```
Testing Date: _______________
Tester: _______________
Django Version: _______________
Database: _______________
Browser: _______________

Total Tests: ___
Passed: ___
Failed: ___
Skipped: ___

Issues Found:
1. ___________________________
2. ___________________________
3. ___________________________

Notes:
________________________________
________________________________

Sign-off: ___________ Date: ___________
```

---

## Cleanup After Testing

- [ ] Delete test categories created during testing
- [ ] Delete test supplies created during testing
- [ ] Reset database to clean state if needed
- [ ] Clear browser cache
- [ ] Log out from all test accounts

---

## Success Criteria

✅ **Feature is ready for production when:**
- [ ] All 100+ tests pass
- [ ] No blocking issues found
- [ ] Performance meets requirements
- [ ] Accessibility verified
- [ ] Browser compatibility confirmed
- [ ] Documentation complete
- [ ] User training done
- [ ] Stakeholder approval obtained
