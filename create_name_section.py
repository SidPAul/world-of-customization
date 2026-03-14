import os
import sys
import django

# Setup Django environment
sys.path.append(r'd:\Sem6')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from products.models import Product, Category

def create_name_board_section():
    new_cat_name = "Name Boards & Signage"
    
    # Create the new category
    category, created = Category.objects.get_or_create(
        name=new_cat_name,
        defaults={'description': 'Customized office and home name boards, nameplates, and signage.'}
    )
    
    # Products to move
    search_terms = ['Name Board', 'Name Stand', 'Nameplate']
    moved_count = 0
    
    for term in search_terms:
        products = Product.objects.filter(name__icontains=term)
        for p in products:
            if p.category != category:
                old_cat = p.category.name
                p.category = category
                p.save()
                print(f"Moved '{p.name}' from '{old_cat}' to '{new_cat_name}'")
                moved_count += 1
                
    print(f"Successfully moved {moved_count} products to the new section.")

if __name__ == '__main__':
    create_name_board_section()
