from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Supply, SupplyRequest, SupplyCategory, BorrowedItem
from django.db.models import Q

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'role', 'department', 'phone')
        widgets = {
            'role': forms.Select(attrs={'class': 'form-select'}),
            'department': forms.TextInput(attrs={'class': 'form-input'}),
            'phone': forms.TextInput(attrs={'class': 'form-input'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make role required
        self.fields['role'].required = True
        # Remove admin option from role choices
        role_choices = [choice for choice in self.fields['role'].choices if choice[0] != 'admin']
        self.fields['role'].choices = role_choices
        # Add help text
        self.fields['role'].help_text = "Select your role in the organization"
        self.fields['department'].help_text = "Your department or division (optional)"
        self.fields['phone'].help_text = "Your phone number (optional)"
    
    def save(self, commit=True):
        user = super().save(commit=False)
        # Set approval status based on role
        if user.role in ['gso_staff', 'department_user']:
            user.approval_status = 'pending'
        else:
            user.approval_status = 'approved'
        
        if commit:
            user.save()
        return user

class SupplyForm(forms.ModelForm):
    # Add explicit supply type field for better UX
    supply_type = forms.ChoiceField(
        label='Supply Type',
        choices=[
            (False, '📦 Non-Consumable (Equipment) - Reusable items like printers, mice, keyboards'),
            (True, '💧 Consumable (Supplies) - Disposable items like paper, pens, ink'),
        ],
        widget=forms.RadioSelect(attrs={'class': 'form-radio'}),
        help_text='Select whether this item is equipment that can be reused or supplies that get consumed',
        required=True,
    )
    
    # Add field for creating new category if needed
    new_category = forms.CharField(
        label='Create New Category',
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Enter category name (e.g., Electronics, Office Supplies)',
            'id': 'new_category_input'
        }),
        help_text='Leave blank to use existing category above'
    )
    

    # Redeclare numeric fields as CharField to allow commas
    quantity = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-input comma-formatted', 'inputmode': 'numeric'}),
        required=True
    )
    min_stock_level = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-input comma-formatted', 'inputmode': 'numeric'}),
        required=True
    )
    cost_per_unit = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-input comma-formatted', 'inputmode': 'decimal'}),
        required=False
    )
    amount = forms.CharField(
        label='Total Purchase Amount (₱)',
        widget=forms.TextInput(attrs={'class': 'form-input comma-formatted', 'placeholder': 'Total purchase amount', 'inputmode': 'decimal'}),
        required=False,
        help_text="Total cost of purchase"
    )

    class Meta:
        model = Supply
        fields = ['name', 'description', 'category', 'quantity', 'min_stock_level', 'unit', 'cost_per_unit', 'serial_number', 'date_purchased', 'amount', 'location', 'image', 'supply_type']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g., USB Flash Drive 32GB'}),
            'description': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 3, 'placeholder': 'Describe this supply...'}),
            'category': forms.Select(attrs={'class': 'form-select', 'id': 'category_select'}),
            # quantity, min_stock_level, cost_per_unit, amount are handled by class fields above
            'unit': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g., pieces, reams, bottles'}),
            'serial_number': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g., SN123456789'}),
            'date_purchased': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
            'location': forms.TextInput(attrs={'class': 'form-input'}),
            'image': forms.FileInput(attrs={'class': 'form-input', 'accept': 'image/*'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set initial value for supply_type if editing existing supply
        if self.instance and self.instance.pk:
            self.fields['supply_type'].initial = str(self.instance.is_consumable)
        else:
            # Default to Non-Consumable for new supplies
            self.fields['supply_type'].initial = 'False'
    
    def clean_quantity(self):
        data = self.cleaned_data['quantity']
        if isinstance(data, str):
            data = data.replace(',', '')
        if not data:
            return 0
        try:
            return int(data)
        except ValueError:
            raise forms.ValidationError("Please enter a valid integer.")

    def clean_min_stock_level(self):
        data = self.cleaned_data['min_stock_level']
        if isinstance(data, str):
            data = data.replace(',', '')
        if not data:
            return 0
        try:
            return int(data)
        except ValueError:
            raise forms.ValidationError("Please enter a valid integer.")

    def clean_cost_per_unit(self):
        data = self.cleaned_data['cost_per_unit']
        if isinstance(data, str):
            data = data.replace(',', '')
        if not data:
            return 0.00
        try:
            return float(data)
        except ValueError:
            raise forms.ValidationError("Please enter a valid number.")

    def clean_amount(self):
        data = self.cleaned_data['amount']
        if isinstance(data, str):
            data = data.replace(',', '')
        if not data:
            return 0.00
        try:
            return float(data)
        except ValueError:
            raise forms.ValidationError("Please enter a valid number.")

    def clean(self):
        cleaned_data = super().clean()
        supply_type = cleaned_data.get('supply_type')
        new_category = cleaned_data.get('new_category', '').strip()
        category = cleaned_data.get('category')
        
        # Convert string representation to boolean
        if supply_type is not None:
            cleaned_data['is_consumable'] = supply_type == 'True'
        
        # Validate category selection
        if new_category:
            # If new category is provided, we'll create it in save()
            # But validate that it's not empty
            if len(new_category) < 2:
                raise forms.ValidationError('Category name must be at least 2 characters long.')
        elif not category:
            # If no new category and no existing category selected
            raise forms.ValidationError('Please either select an existing category or create a new one.')
        
        return cleaned_data
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        # Set the is_consumable field based on supply_type
        supply_type = self.cleaned_data.get('supply_type')
        instance.is_consumable = supply_type == 'True'
        
        # Handle new category creation
        new_category = self.cleaned_data.get('new_category', '').strip()
        if new_category:
            # Create new category or get existing one with that name
            category, created = SupplyCategory.objects.get_or_create(
                name=new_category,
                defaults={'description': f'Created for {instance.name}'}
            )
            instance.category = category
        
        if commit:
            instance.save()
        return instance

class SupplyRequestForm(forms.ModelForm):
    class Meta:
        model = SupplyRequest
        fields = ['supply', 'quantity_requested', 'purpose']
        widgets = {
            'supply': forms.Select(attrs={'class': 'form-select'}),
            'quantity_requested': forms.NumberInput(attrs={'class': 'form-input'}),
            'purpose': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            # Filter supplies - only CONSUMABLE items with available stock
            supply_field = self.fields['supply']
            supply_field.queryset = Supply.objects.filter(quantity__gt=0, is_consumable=True).order_by('name')
            
            # Build choices with quantity info
            choices = [('', '-- Select a consumable supply --')]
            for supply in supply_field.queryset:
                label = f"{supply.name} ({supply.quantity} {supply.unit} available)"
                choices.append((supply.pk, label))
            
            supply_field.choices = choices

class SupplyCategoryForm(forms.ModelForm):
    class Meta:
        model = SupplyCategory
        fields = ['name', 'description', 'is_material']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input'}),
            'description': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 3}),
        }

class QRScanForm(forms.Form):
    qr_data = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-input',
        'placeholder': 'Scan QR code or enter supply ID',
        'autofocus': True
    }))
    action = forms.ChoiceField(choices=[
        ('scan', 'Scan'),
        ('issue', 'Issue'),
        ('return', 'Return')
    ], widget=forms.Select(attrs={'class': 'form-select'}))
    location = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-input',
        'placeholder': 'Location'
    }))
    notes = forms.CharField(required=False, widget=forms.Textarea(attrs={
        'class': 'form-textarea',
        'rows': 3,
        'placeholder': 'Additional notes (optional)'
    }))

class BorrowRequestForm(forms.ModelForm):
    """Form for requesting to borrow items - requires GSO approval"""
    borrow_duration_days = forms.IntegerField(
        min_value=1,
        initial=3,
        label="Duration (Days)",
        help_text="Number of days to borrow the item",
        widget=forms.NumberInput(attrs={
            'class': 'form-input',
            'min': '1',
            'value': '3'
        })
    )
    
    class Meta:
        model = SupplyRequest
        fields = ['supply', 'quantity_requested', 'requested_location', 'purpose']
        widgets = {
            'supply': forms.Select(attrs={'class': 'form-select', 'id': 'supply-select'}),
            'quantity_requested': forms.NumberInput(attrs={'class': 'form-input', 'min': '1'}),
            'purpose': forms.Textarea(attrs={
                'class': 'form-textarea',
                'rows': 3,
                'placeholder': 'Describe why you need to borrow this item...'
            }),
            'requested_location': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Location where the equipment will be used (optional)'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter supplies - include NON-CONSUMABLE items (equipment) and any
        # supplies categorized as "materials" even if their is_consumable flag varies.
        supply_field = self.fields['supply']
        supply_field.queryset = Supply.objects.filter(
            quantity__gt=0
        ).filter(
            Q(is_consumable=False) | Q(category__is_material=True)
        ).order_by('name')
        
        # Build choices with quantity info
        choices = [('', '-- Select equipment to borrow --')]
        for supply in supply_field.queryset:
            label = f"{supply.name} ({supply.quantity} {supply.unit} available)"
            choices.append((supply.pk, label))
        
        supply_field.choices = choices

class BorrowedItemForm(forms.ModelForm):
    """Form for GSO staff to create borrowed item record after approval"""
    class Meta:
        model = BorrowedItem
        fields = ['borrowed_date', 'borrow_duration_days', 'location_when_borrowed', 'notes']
        widgets = {
            'borrowed_date': forms.DateInput(attrs={
                'class': 'form-input',
                'type': 'date',
                'required': True
            }),
            'borrow_duration_days': forms.NumberInput(attrs={
                'class': 'form-input',
                'min': '1',
                'value': '3',
            }),
            'location_when_borrowed': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Location of the item'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-textarea',
                'rows': 3,
                'placeholder': 'Additional notes (optional)'
            }),
        }

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone', 'profile_picture']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-input'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input'}),
            'email': forms.EmailInput(attrs={'class': 'form-input'}),
            'phone': forms.TextInput(attrs={'class': 'form-input'}),
            'profile_picture': forms.FileInput(attrs={'class': 'form-input', 'accept': 'image/jpeg,image/png'}),
        }

class StockAdjustmentForm(forms.Form):
    """Form for adjusting stock due to lost or damaged items"""
    ADJUSTMENT_TYPE_CHOICES = [
        ('lost', '❌ Lost Item'),
        ('damaged', '⚠️ Damaged Item'),
    ]
    
    supply = forms.ModelChoiceField(
        queryset=Supply.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Supply Item'
    )
    
    adjustment_type = forms.ChoiceField(
        choices=ADJUSTMENT_TYPE_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'form-radio'}),
        label='Adjustment Type'
    )
    
    quantity = forms.IntegerField(
        min_value=1,
        widget=forms.NumberInput(attrs={
            'class': 'form-input',
            'min': '1',
            'placeholder': 'Number of items'
        }),
        label='Quantity Affected'
    )
    
    reason = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-textarea',
            'rows': 4,
            'placeholder': 'Describe what happened to the item(s)...'
        }),
        label='Details',
        help_text='Please provide details about how the item was lost or damaged'
    )