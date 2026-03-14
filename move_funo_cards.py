import os
import sys
import django

# Setup Django environment
sys.path.append(r'd:\Sem6')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from products.models import Product, Category

def move_product():
    product_name = "FUNO Cards – The Ultimate Personalized Card Game!"
    category_name = "Games & Fun"
    
    # Get or create the category
    category, _ = Category.objects.get_or_create(
        name=category_name,
        defaults={'description': 'Exciting games and fun personalized items.'}
    )
    
    # Find the product
    p = Product.objects.filter(name__icontains="FUNO Cards").first()
    
    if p:
        old_cat = p.category.name
        p.category = category
        p.save()
        print(f"Successfully moved '{p.name}' from '{old_cat}' to '{category.name}'")
    else:
        print(f"Product '{product_name}' not found")

if __name__ == '__main__':
    move_product()
