# Testing the Modal View Implementation

## How to Test

### 1. Start the Development Server
```bash
python manage.py runserver
```

### 2. Navigate to the Tracking Page
- Go to: `http://127.0.0.1:8000/analytics/requestor-borrower/`
- Must be logged in as admin or gso_staff user

### 3. Test the Modal Functionality

#### Test 1: Open Modal
1. In the "Department Users" table, find any user row
2. Click the blue "View" button
3. **Expected**: 
   - Modal opens with semi-transparent background
   - User's avatar, name, and department appear in modal header
   - Loading spinner briefly appears
   - User's analytics summary loads

#### Test 2: View User Statistics in Modal
1. Modal should display:
   - **Total Requests** card with breakdown:
     - Number of Approved requests
     - Number of Pending requests
     - Number of Rejected requests
   - **Borrowing Activity** card with breakdown:
     - Number of Returned items
     - Number of Unreturned items
     - Number of Overdue items
   - **Approval Rate** with visual progress bar
   - **Department** information
   - **Most Requested Items** list (if any)
   - **Recent Requests** list (if any)

#### Test 3: Close Modal
1. **Method 1**: Click the X button in modal header
   - Modal closes smoothly
   
2. **Method 2**: Click the background (dark overlay)
   - Modal closes smoothly
   
3. **Method 3**: Click "Close" button at bottom
   - Modal closes smoothly

**Expected**: Modal closes and you're back on the tracking page with same user logged in

#### Test 4: View Full Analytics
1. In the open modal, click "View Full Analytics" button
2. **Expected**: Navigates to the full analytics page for that user

#### Test 5: Multiple Users
1. Close the modal (using any method)
2. Click "View" button on a different user
3. **Expected**: 
   - Modal updates with new user's data
   - Avatar colors may change based on username
   - Statistics refresh for new user

## Expected Behavior

| Action | Before | After |
|--------|--------|-------|
| Click View button | Redirects to new page | Opens modal on same page |
| User stays logged in | Yes | Yes ✓ |
| Can view multiple users quickly | No (requires back button) | Yes ✓ |
| URL changes | Yes | No ✓ |
| Session context preserved | Yes | Yes ✓ |

## Browser Console

Check browser developer console (F12) for:
- No JavaScript errors
- AJAX request to `/analytics/user/<id>/modal/` should return HTML
- Status code should be 200 OK

## Files Modified

1. `templates/inventory/tracking/requestor_borrower_tracking.html`
   - Changed View button from link to button
   - Added modal HTML structure
   - Added JavaScript functions

2. `inventory/analytics_views.py`
   - Added `user_analytics_modal()` view function

3. `inventory/urls.py`
   - Added URL route for modal endpoint

## New Files Created

1. `templates/inventory/tracking/partials/user_analytics_modal.html`
   - Modal content template with statistics cards

## Troubleshooting

### Modal doesn't open
- Check browser console for JavaScript errors
- Verify user has admin/gso_staff role
- Check network tab to see if AJAX request succeeds

### Modal shows error message
- Check server logs for exceptions
- Verify user ID is valid
- Ensure user exists with role='department_user'

### Statistics appear wrong
- Verify data in database matches expectations
- Check if date ranges are applied correctly
- Ensure requests and borrowed items belong to correct user

### Styling issues
- Check if Tailwind CSS is properly loaded
- Verify no CSS conflicts with existing styles
- Check browser zoom level
