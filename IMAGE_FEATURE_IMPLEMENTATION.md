# Supply Item Image Implementation

## Overview
Added image upload functionality for supply items in the inventory management system. Users can now upload product images when creating or editing supplies, with preview functionality and display on the supply detail page.

## Changes Made

### 1. Database Model Update (inventory/models.py)
- Added `image` field to the `Supply` model:
  - Type: `ImageField`
  - Upload path: `supply_images/`
  - Nullable and blank: Yes
  - Help text: "Product image or photo"

### 2. Form Updates (inventory/forms.py)
- Updated `SupplyForm` to include the `image` field
- Added file input widget with image file type validation (`accept="image/*"`)
- Added to form fields list: `['name', 'description', 'category', 'quantity', 'min_stock_level', 'unit', 'cost_per_unit', 'location', 'image', 'supply_type']`

### 3. Supply Form Template (templates/inventory/supply_form.html)
- Added new **Product Image** section (Section 3a) with:
  - **Current Image Display**: Shows existing image with option to remove
  - **File Input**: Accepts image files (JPG, PNG, GIF, WebP)
  - **Image Preview**: Live preview of selected image with file size
  - **File Size Validation**: Client-side validation (max 5MB)
  - **Alpine.js Component**: `imageUpload()` function handles preview and validation

### 4. Supply Detail Template (templates/inventory/supply_detail.html)
- **Updated Header**: Shows product image (24x24px) next to supply name if available
  - Falls back to box icon if no image
  - Image is clickable and links to detail page
- **Product Image Section**: New sidebar card displaying:
  - Full-size product image with rounded corners and border
  - Download button for image
  - Shown only if image exists

### 5. Supply List Template (templates/inventory/partials/supply_list.html)
- Updated supply thumbnail column to display actual product image
- Image dimensions: 10x10px, rounded corners
- Falls back to box icon if no image
- Images have border and use object-cover for proper scaling

### 6. Database Migration
- Created migration: `0017_remove_supplyrequest_group_id_and_more.py`
- Adds the `image` field to the Supply table
- Migration applied successfully

## Features

### Image Upload
- **File Format Support**: JPG, PNG, GIF, WebP
- **File Size Limit**: 5MB (enforced client-side with JavaScript validation)
- **Image Preview**: Real-time preview showing selected image and file size
- **Optional**: Image is completely optional - supplies can exist without images

### Image Display
- **List View**: Thumbnail (10x10px) next to supply name
- **Detail View**: 
  - Header thumbnail (24x24px)
  - Full-size image in sidebar with download option
- **Fallback**: Box icon appears if no image is set

### Image Management
- **Upload**: New images can be uploaded when creating or editing supplies
- **Replace**: Upload new image to replace existing one
- **Remove**: Checkbox to remove current image while editing
- **Download**: Download button on detail page to save image locally

## File Structure
```
media/
├── supply_images/           # New directory for product images
│   ├── [item_id]_image.jpg
│   ├── [item_id]_image.png
│   └── ...

templates/
├── inventory/
│   ├── supply_form.html     # Updated with image section
│   ├── supply_detail.html   # Updated with image display
│   └── partials/
│       └── supply_list.html # Updated with image thumbnails
```

## Technical Implementation

### Alpine.js Component
```javascript
function imageUpload() {
    return {
        preview: '',      // Base64 preview of selected image
        fileSize: '',     // Human-readable file size
        
        previewImage(event) {
            // Validates file size (5MB max)
            // Converts to base64 for preview
            // Displays file size to user
        }
    }
}
```

### Image Display
- Uses Django's `ImageField` with automatic path management
- Images stored in `MEDIA_ROOT/supply_images/`
- Accessible via `supply.image.url` in templates
- Responsive: Uses CSS object-cover for proper scaling
- Rounded corners and borders for visual consistency

## Settings Configuration
Existing media file settings in `supply_/settings.py`:
- `MEDIA_URL = '/media/'`
- `MEDIA_ROOT = os.path.join(BASE_DIR, 'media')`

No changes needed - uses existing media configuration.

## Usage Instructions

### As Admin/GSO Staff
1. **Creating Supply**:
   - Navigate to Create Supply page
   - Fill basic information
   - In "Product Image" section, click file input
   - Select image file (JPG/PNG/GIF/WebP, max 5MB)
   - See preview with file size
   - Submit form

2. **Editing Supply**:
   - Navigate to supply detail or edit page
   - View current image in image section
   - Option to remove current image with checkbox
   - Upload new image to replace
   - Changes saved on form submission

3. **Viewing Images**:
   - Supply list shows thumbnail images next to names
   - Supply detail page displays full image in sidebar
   - Download button available for saving image

### As Department User
- Can see product images in supply list and detail views
- Cannot upload or modify images
- Can download images for reference

## Benefits
1. **Better Identification**: Visual representation helps identify supplies quickly
2. **Improved Usability**: Users can see what items look like before requesting/borrowing
3. **Reference Documentation**: Images serve as visual documentation
4. **Downloadable**: Users can save images for records
5. **Optional**: Doesn't break existing supplies without images
6. **Performance**: Lightweight thumbnails in list view, full image in detail view

## Browser Support
- Works in all modern browsers that support:
  - HTML5 File API
  - FileReader API
  - Canvas/Image rendering
- Fallback to box icon for supplies without images

## Future Enhancements
- Multiple images per supply (gallery)
- Image cropping before upload
- Image compression during upload
- Image drag-and-drop upload
- Lightbox/modal view for full-size images
- Image rotation/orientation fixes
- Batch image upload with CSV import

## Testing Checklist
- [ ] Create supply with image
- [ ] Create supply without image
- [ ] Edit supply and change image
- [ ] Edit supply and remove image
- [ ] View supply list with mixed images/no images
- [ ] View supply detail page with image
- [ ] Download image from detail page
- [ ] Test image preview with large file (>5MB)
- [ ] Test with various image formats (JPG, PNG, GIF, WebP)
- [ ] Test on mobile/tablet devices
- [ ] Verify responsive image display

## Database Query Impact
- Minimal: Only adds one optional field per supply
- No indexing on image field needed
- Image storage is filesystem-based, not database-stored
