# Borrowing Duration Implementation

## Overview
This implementation adds a date-based borrowing duration feature where users must select the date they're borrowing an item and automatically get a 3-day return deadline (configurable).

## Changes Made

### 1. **Database Model Updates** (`inventory/models.py`)

#### BorrowedItem Model
- **New Field**: `borrowed_date` - DateField to store the date when the item was borrowed
- **Updated Field**: `return_deadline` - Changed from DateTimeField to DateField for simpler date-based tracking
- **New Field**: `borrow_duration_days` - PositiveIntegerField (default: 3) to set the borrow duration
- **New Method**: `save()` - Automatically calculates `return_deadline` from `borrowed_date` + `borrow_duration_days`

#### Updated Properties
- `is_overdue` - Now compares dates instead of datetimes
- `days_until_due` - Simplified to work with dates
- `due_in_days` - Simplified to work with dates
- `due_status` - Updated to use date comparisons

#### Notification Model
- Removed incorrect save method that was trying to set `return_deadline`

### 2. **Database Migration** (`inventory/migrations/0007_borrowing_duration_fields.py`)

Created a migration that:
- Adds `borrowed_date` field to BorrowedItem
- Adds `borrow_duration_days` field with default value of 3
- Changes `return_deadline` from DateTimeField to DateField
- Runs data migration to populate `borrowed_date` from `borrowed_at` for existing records
- Runs data migration to calculate `return_deadline` for existing records

### 3. **Forms** (`inventory/forms.py`)

#### New BorrowedItemForm
- Fields: `supply`, `borrowed_quantity`, `borrowed_date`, `borrow_duration_days`, `location_when_borrowed`, `notes`
- Date picker widget for `borrowed_date`
- Number input for `borrow_duration_days` with default value of 3
- All fields have appropriate Tailwind CSS classes for styling

### 4. **Views** (`inventory/views.py`)

#### Updated `request_borrow_item` View
- Changed from a request-based approach to direct borrowing with date selection
- Users must select:
  - Which item to borrow
  - Quantity
  - The date they're borrowing it (defaults to today)
  - Duration in days (defaults to 3)
  - Location and optional notes

- On submission:
  1. Creates a BorrowedItem record (which auto-calculates return_deadline)
  2. Creates a corresponding SupplyRequest for tracking
  3. Updates the supply quantity
  4. Logs an inventory transaction
  5. Shows success message with the return deadline

- Validation:
  - Prevents borrowing if user has overdue items
  - Only shows supplies with available quantity

### 5. **Templates**

#### request_borrow_item.html (New)
- Updated borrowing form template with:
  - Date input for selecting borrow date
  - Duration input with default value of 3
  - JavaScript to calculate and display return deadline in real-time
  - Default date set to today
  - Clear information about the borrowing process
  - Styling with Tailwind CSS

#### partials/borrowed_items_list.html (Updated)
- Added new "Borrow Date" column to show when the item was borrowed
- Added new "Return Deadline" column showing:
  - The return deadline date
  - Status indicator (OVERDUE, DUE TODAY, Due soon, Returned)
  - Color-coded for quick visual reference
- Simplified status column with icons
- Removed time-based deadline displays since we're now using dates

## Key Features

1. **Date-Based Tracking**: Users select the exact date of borrowing
2. **Automatic Deadline Calculation**: Return deadline = borrow date + duration (default 3 days)
3. **Real-Time Feedback**: JavaScript shows calculated return date as user enters data
4. **Overdue Prevention**: Users with overdue items can't borrow more items
5. **Clear Deadline Display**: Return deadlines are prominently displayed in the borrowed items list
6. **Color-Coded Status**: 
   - Red for overdue
   - Yellow for due today
   - Amber for due soon
   - Green for returned
   - Blue for actively borrowed

## How It Works

1. User navigates to "Borrow Item" page
2. Selects an item from the available supplies list
3. Enters quantity to borrow
4. Selects the date they're borrowing it (defaults to today)
5. Selects the duration (defaults to 3 days)
6. Optionally adds location and notes
7. Submits the form
8. System calculates return deadline automatically
9. Item is added to "My Borrowed Items"
10. User can track the return deadline

## Return Deadline Calculation

```
Return Deadline = Borrow Date + Duration Days
Example: If borrowed on 2025-01-15 with 3-day duration
         Return Deadline = 2025-01-18
```

## Database Compatibility

The migration handles:
- Existing borrowed items (sets borrowed_date from borrowed_at)
- Existing return deadlines (if set)
- New records get automated deadline calculation

## Testing Recommendations

1. Test borrowing with different dates
2. Test with different durations
3. Verify overdue items prevent new borrowing
4. Check that return deadline is calculated correctly
5. Verify the migration works on existing database
6. Test the real-time JavaScript deadline display

## Future Enhancements

- Add configurable default duration per item type
- Send notifications before due date
- Auto-calculate late fees if implemented
- Add extension requests
- Integration with calendar view
