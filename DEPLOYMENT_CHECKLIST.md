# Deployment Checklist: Consumable vs Non-Consumable Items

## Pre-Deployment

### Code Review
- [ ] All Python code reviewed and tested
- [ ] All JavaScript code syntax verified
- [ ] HTML/Template code validated
- [ ] No console errors when running locally
- [ ] No broken links in templates

### Testing
- [ ] Local migration test passed
- [ ] Form rendering works correctly
- [ ] Item selection works with radio buttons
- [ ] Selection updates panel in real-time
- [ ] Quantity validation works
- [ ] Form submission works
- [ ] Mobile responsive design tested
- [ ] Browser compatibility checked (Chrome, Firefox, Safari, Edge)

### Documentation
- [ ] IMPLEMENTATION_SUMMARY.txt created
- [ ] CONSUMABLE_NONCONSUMABLE_SEPARATION.md created
- [ ] QUICK_START.md created
- [ ] VISUAL_GUIDE.md created
- [ ] DEPLOYMENT_CHECKLIST.md created
- [ ] Code comments added where needed

## Deployment Steps

### Step 1: Backup Database
```bash
# Create backup before running migration
python manage.py dumpdata > backup_before_consumable_feature.json
```
- [ ] Backup created successfully
- [ ] Backup file verified

### Step 2: Deploy Code
```bash
# Pull latest code or upload files
git pull origin main
# OR manually upload files
```

Files to deploy:
- [ ] `inventory/models.py` - Updated Supply model
- [ ] `inventory/forms.py` - Updated forms
- [ ] `inventory/views.py` - Updated view
- [ ] `templates/inventory/request_borrow_item.html` - New template
- [ ] `inventory/migrations/0008_supply_is_consumable.py` - Migration file
- [ ] `setup_consumable_types.py` - Helper script

### Step 3: Apply Migrations
```bash
python manage.py migrate
```
- [ ] Migration completed without errors
- [ ] Database structure updated
- [ ] No rollback needed

### Step 4: Classify Items (Choose One)

#### Option A: Auto-Classification
```bash
python manage.py shell < setup_consumable_types.py
```
- [ ] Script ran successfully
- [ ] Check results output
- [ ] Verify items are classified correctly

#### Option B: Manual Classification
```
1. Go to Admin: /admin
2. Select "Supplies"
3. For each item, check "Is Consumable" if appropriate
4. Save
```
- [ ] All items classified
- [ ] At least some items in each category
- [ ] Verification done

### Step 5: Test in Production Environment
- [ ] Access Request to Borrow page
- [ ] Verify two sections appear
- [ ] Test item selection
- [ ] Test form submission
- [ ] Test with multiple browsers
- [ ] Test on mobile device
- [ ] Verify availability display
- [ ] Check error handling

### Step 6: Monitoring
```bash
# Check logs for errors
tail -f /var/log/django/error.log
```
- [ ] No errors in application logs
- [ ] No database errors
- [ ] No JavaScript console errors
- [ ] User feedback positive (if applicable)

## Post-Deployment

### Verification Checklist
- [ ] Users can access "Request to Borrow Item" page
- [ ] Non-consumable items visible in first section
- [ ] Consumable items visible in second section
- [ ] Selection updates display correctly
- [ ] Quantity input validates properly
- [ ] Form submits successfully
- [ ] Admin can edit "Is Consumable" field

### User Communication
- [ ] Admin notified of changes
- [ ] Users notified of new interface (if needed)
- [ ] Documentation shared with team
- [ ] Training completed (if needed)

### Monitoring
- [ ] Set up error monitoring
- [ ] Monitor database size increase
- [ ] Monitor page load times
- [ ] Check for any performance issues

## Rollback Plan (If Needed)

### Quick Rollback
```bash
# Revert migration
python manage.py migrate inventory 0007_borrowing_duration_fields

# Restore previous code
git checkout previous_commit_hash
# OR manually restore backup files

# Restore database
python manage.py loaddata backup_before_consumable_feature.json
```

### Rollback Checklist
- [ ] Backup file accessible
- [ ] Previous code version available
- [ ] Rollback tested locally first
- [ ] Rollback procedure documented
- [ ] Team informed of rollback plan

## Performance Checks

### After Deployment
- [ ] Page load time acceptable (< 2 seconds)
- [ ] Database queries optimized
- [ ] No N+1 query problems
- [ ] JavaScript bundle size reasonable
- [ ] CSS file size acceptable
- [ ] Image loading optimized

## Security Checks

- [ ] CSRF tokens present in forms
- [ ] SQL injection prevention (using ORM)
- [ ] XSS prevention (template escaping)
- [ ] Authorization checks in place
- [ ] Input validation working
- [ ] Rate limiting applied (if needed)

## Accessibility Checks

- [ ] Keyboard navigation works
- [ ] Screen reader compatible
- [ ] Color contrast sufficient
- [ ] Form labels accessible
- [ ] Error messages clear
- [ ] Mobile touch targets adequate (44x44px)

## Browser Compatibility

Test in each browser:

### Desktop
- [ ] Chrome (latest)
- [ ] Firefox (latest)
- [ ] Safari (latest)
- [ ] Edge (latest)
- [ ] IE 11 (if needed)

### Mobile
- [ ] Chrome on Android
- [ ] Safari on iOS
- [ ] Firefox on Android

## API/Integration Tests

If integrated with other systems:
- [ ] API endpoints working
- [ ] Data sync working
- [ ] External integrations working
- [ ] Webhooks firing correctly

## Analytics

Set up tracking for:
- [ ] Feature adoption
- [ ] Error rates
- [ ] User feedback
- [ ] Performance metrics
- [ ] Database size growth

## Documentation Updates

- [ ] Update internal wiki/knowledge base
- [ ] Update API documentation
- [ ] Update changelog
- [ ] Update user guides
- [ ] Update admin guides

## Sign-Off

- [ ] Development team approval: ________________
- [ ] QA team approval: ________________
- [ ] Product owner approval: ________________
- [ ] DevOps approval: ________________

## Final Notes

```
Deployment Date: _______________
Deployed By: _______________
Verified By: _______________
Notes: ___________________________________________________
_________________________________________________________
_________________________________________________________
```

## Post-Deployment Support

### First 24 Hours
- [ ] Monitor error logs
- [ ] Check user feedback
- [ ] Respond to issues quickly
- [ ] Have rollback plan ready

### First Week
- [ ] Gather performance metrics
- [ ] Collect user feedback
- [ ] Monitor database growth
- [ ] Check for edge cases

### Ongoing
- [ ] Regular monitoring
- [ ] User support
- [ ] Documentation maintenance
- [ ] Performance optimization

---

**Deployment completed successfully when all checkboxes are marked ✓**
