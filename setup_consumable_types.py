"""
Script to classify existing supplies as consumable or non-consumable
Run with: python manage.py shell < setup_consumable_types.py
"""

from inventory.models import Supply

# List of consumable item keywords
CONSUMABLE_KEYWORDS = [
    'paper', 'pen', 'pencil', 'stapler', 'staple', 'ink', 'toner', 'cartridge',
    'disinfectant', 'spray', 'wax', 'cleaner', 'soap', 'sanitizer', 'paste',
    'glue', 'tape', 'post-it', 'notebook', 'pad', 'label', 'sticker', 'marker',
    'highlighter', 'eraser', 'rubber', 'blade', 'cutter', 'marker', 'whiteboard',
    'board', 'sticky', 'adhesive', 'bottle', 'liquid', 'chemical'
]

def classify_supplies():
    """Classify supplies based on keywords"""
    supplies = Supply.objects.all()
    updated_count = 0
    
    for supply in supplies:
        name_lower = supply.name.lower()
        description_lower = supply.description.lower()
        
        # Check if the supply name or description contains consumable keywords
        is_consumable = any(
            keyword in name_lower or keyword in description_lower 
            for keyword in CONSUMABLE_KEYWORDS
        )
        
        if is_consumable != supply.is_consumable:
            supply.is_consumable = is_consumable
            supply.save()
            print(f"Updated: {supply.name} -> is_consumable={is_consumable}")
            updated_count += 1
    
    print(f"\nTotal items updated: {updated_count}")
    print(f"Consumable items: {Supply.objects.filter(is_consumable=True).count()}")
    print(f"Non-consumable items: {Supply.objects.filter(is_consumable=False).count()}")

# Run the classification
classify_supplies()
