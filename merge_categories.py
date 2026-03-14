import os
import sys
import django

# Setup Django environment
sys.path.append(r'd:\Sem6')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from products.models import Product, Category

def merge_home_decor():
    old_name = "Home Decor"
    new_name = "Home & Decor"
    
    # Get or create the target category
    target_category, created = Category.objects.get_or_create(
        name=new_name,
        defaults={'description': 'Premium home and decor items for customization.'}
    )
    
    # Get the source category
    try:
        source_category = Category.objects.get(name=old_name)
        
        # Move all products
        products_to_move = Product.objects.filter(category=source_category)
        count = products_to_move.count()
        
        if count > 0:
            products_to_move.update(category=target_category)
            print(f"Moved {count} products from '{old_name}' to '{new_name}'")
        else:
            print(f"No products found in '{old_name}'")
            
        # Delete the old category
        source_category.delete()
        print(f"Deleted category: '{old_name}'")
        
    except Category.DoesNotExist:
        print(f"Source category '{old_name}' not found. It might have already been removed.")

if __name__ == '__main__':
    merge_home_decor()
