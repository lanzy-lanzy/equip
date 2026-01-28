# Steps to Apply the Borrowing Duration Feature

## Prerequisites
- Django project is running and database is accessible
- All existing migrations have been applied

## Steps

### 1. Apply the Database Migration
```bash
python manage.py migrate
```

This will:
- Add `borrowed_date` field to BorrowedItem
- Add `borrow_duration_days` field (default: 3)
- Convert `return_deadline` from DateTimeField to DateField
- Populate `borrowed_date` from existing `borrowed_at` values
- Calculate `return_deadline` for existing borrowed items

### 2. Verify the Changes
Check the database to ensure fields were added correctly:
```bash
python manage.py shell
>>> from inventory.models import BorrowedItem
>>> item = BorrowedItem.objects.first()
>>> print(item.borrowed_date)  # Should show a date
>>> print(item.return_deadline)  # Should show a date
>>> print(item.borrow_duration_days)  # Should show 3 (or whatever was set)
```

### 3. Test the Feature

#### Via Admin Interface
1. Navigate to Django admin
2. Try adding a new BorrowedItem
3. You should see the new fields:
   - `borrowed_date` (date picker)
   - `borrow_duration_days` (number input, default 3)

#### Via Web Interface
1. Log in as a department user
2. Navigate to "Borrow Item" page
3. Fill in the borrowing form with:
   - Select an item
   - Enter quantity
   - Pick a borrow date
   - Enter duration (or use default 3)
   - Click "Confirm Borrow"
4. You should see the item in "My Borrowed Items" list
5. Check that the return deadline is calculated correctly

### 4. Verify Return Deadline Calculation
- Borrow Date: 2025-01-15
- Duration: 3 days
- Expected Return Deadline: 2025-01-18

Check in the database or admin interface that the calculation is correct.

### 5. Check Existing Data
All existing borrowed items should have:
- `borrowed_date` set to the date of `borrowed_at`
- `return_deadline` calculated from `borrowed_date` + 3 days (if not already set)

## Troubleshooting

### Migration Fails
- Ensure all previous migrations are applied: `python manage.py showmigrations`
- Check database permissions
- Check for any custom signals that might interfere

### Fields Not Appearing in Admin
- Restart the Django development server
- Clear browser cache (Ctrl+F5)

### Return Deadline Not Calculated
- The `save()` method in BorrowedItem should handle this
- Manual fix: `python manage.py shell` and manually update records if needed

### Date Display Issues in Templates
- Ensure Django is using the correct date format
- Check browser timezone settings

## Rollback (If Needed)

To revert the migration:
```bash
python manage.py migrate inventory 0006_notification
```

This will:
- Remove the new fields
- Revert `return_deadline` to DateTimeField
- Restore the database to the previous state

## Post-Migration

Once everything is working:
1. Test the borrowing flow with different dates
2. Verify overdue detection works correctly
3. Check that users can't borrow if they have overdue items
4. Monitor the borrowed_items_list template for any display issues
5. Update any API endpoints if they return borrowed items

## Notes

- The borrow_duration_days defaults to 3 (can be changed per item in the form)
- Return deadline is automatically calculated on save
- Users can still manually set return_deadline if needed (admin only)
- The feature works with existing data from before this update
