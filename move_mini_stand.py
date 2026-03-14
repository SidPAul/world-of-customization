import os
import sys
import django

# Setup Django environment
sys.path.append(r'd:\Sem6')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from products.models import Product, Category

def move_name_stand():
    product_name = "Customized Mini Name Stand"
    category_name = "Accessories & Keepsakes"
    
    # Get or create the category
    category, _ = Category.objects.get_or_create(
        name=category_name,
        defaults={'description': 'Premium personalized accessories and tiny keepsakes.'}
    )
    
    # Find the product
    p = Product.objects.filter(name__icontains="Mini Name Stand").first()
    
    if p:
        old_cat = p.category.name
        p.category = category
        p.save()
        print(f"Successfully moved '{p.name}' from '{old_cat}' to '{category.name}'")
    else:
        print(f"Product '{product_name}' not found")

if __name__ == '__main__':
    move_name_stand()
