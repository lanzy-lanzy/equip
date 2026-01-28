from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Sum
from django.core.paginator import Paginator

from .models import InventoryTransaction, Supply
from .forms import StockAdjustmentForm


@login_required
def stock_adjustment_list(request):
    """View list of all stock adjustments (lost/damaged items)"""
    if request.user.role not in ['admin', 'gso_staff']:
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('dashboard')
    
    # Get transactions for lost and damaged items
    transactions = InventoryTransaction.objects.filter(
        transaction_type__in=['lost', 'damaged']
    ).select_related('supply', 'performed_by').order_by('-created_at')
    
    # Filters
    supply_filter = request.GET.get('supply')
    type_filter = request.GET.get('type')
    search = request.GET.get('search', '')
    
    if supply_filter:
        transactions = transactions.filter(supply_id=supply_filter)
    
    if type_filter:
        transactions = transactions.filter(transaction_type=type_filter)
    
    if search:
        transactions = transactions.filter(
            Q(supply__name__icontains=search) |
            Q(reason__icontains=search) |
            Q(performed_by__username__icontains=search)
        )
    
    # Pagination
    paginator = Paginator(transactions, 20)
    page = request.GET.get('page', 1)
    transactions = paginator.get_page(page)
    
    # Stats
    all_adjustments = InventoryTransaction.objects.filter(transaction_type__in=['lost', 'damaged'])
    lost_count = all_adjustments.filter(transaction_type='lost').aggregate(Sum('quantity'))['quantity__sum'] or 0
    damaged_count = all_adjustments.filter(transaction_type='damaged').aggregate(Sum('quantity'))['quantity__sum'] or 0
    
    supplies = Supply.objects.all().order_by('name')
    
    context = {
        'transactions': transactions,
        'supplies': supplies,
        'supply_filter': supply_filter,
        'type_filter': type_filter,
        'search': search,
        'lost_count': lost_count,
        'damaged_count': damaged_count,
    }
    
    return render(request, 'inventory/stock_adjustment_list.html', context)


@login_required
def stock_adjustment_create(request):
    """Create a new stock adjustment for lost or damaged items"""
    if request.user.role not in ['admin', 'gso_staff']:
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = StockAdjustmentForm(request.POST)
        if form.is_valid():
            supply = form.cleaned_data['supply']
            adjustment_type = form.cleaned_data['adjustment_type']
            quantity = form.cleaned_data['quantity']
            reason = form.cleaned_data['reason']
            
            # Check if supply has enough quantity
            if quantity > supply.quantity:
                messages.error(request, f'Cannot adjust {quantity} items. Only {supply.quantity} items available.')
                return render(request, 'inventory/stock_adjustment_form.html', {'form': form})
            
            # Store previous quantity
            previous_quantity = supply.quantity
            
            # Reduce the supply quantity
            supply.quantity -= quantity
            supply.save()
            
            # Create transaction record
            InventoryTransaction.objects.create(
                supply=supply,
                transaction_type=adjustment_type,
                quantity=-quantity,
                previous_quantity=previous_quantity,
                new_quantity=supply.quantity,
                reason=reason,
                performed_by=request.user
            )
            
            adjustment_label = 'Lost' if adjustment_type == 'lost' else 'Damaged'
            messages.success(request, f'Successfully recorded {quantity} item(s) as {adjustment_label.lower()}.')
            return redirect('stock_adjustment_list')
    else:
        form = StockAdjustmentForm()
    
    return render(request, 'inventory/stock_adjustment_form.html', {'form': form})


@login_required
def stock_adjustment_detail(request, pk):
    """View details of a stock adjustment"""
    if request.user.role not in ['admin', 'gso_staff']:
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('dashboard')
    
    transaction = get_object_or_404(
        InventoryTransaction.objects.select_related('supply', 'performed_by'),
        pk=pk,
        transaction_type__in=['lost', 'damaged']
    )
    
    context = {
        'transaction': transaction,
        'is_lost': transaction.transaction_type == 'lost',
        'is_damaged': transaction.transaction_type == 'damaged',
    }
    
    return render(request, 'inventory/stock_adjustment_detail.html', context)
