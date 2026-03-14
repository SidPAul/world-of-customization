import os
import sys
import django

# Setup Django environment
sys.path.append(r'd:\Sem6')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from products.models import Product

def remove_fan_cards():
    name_to_remove = "Fan cards"
    # Search for products with a similar name
    products = Product.objects.filter(name__icontains=name_to_remove)
    
    if products.exists():
        for p in products:
            print(f"Found product: {p.name}")
            # Delete image file if it exists
            if p.image and os.path.isfile(p.image.path):
                try:
                    os.remove(p.image.path)
                    print(f"  Deleted image: {p.image.path}")
                except Exception as e:
                    print(f"  Failed to delete image: {e}")
            
            # Delete the product
            p.delete()
            print(f"Successfully removed product: {p.name}")
    else:
        print(f"Product not found: {name_to_remove}")

if __name__ == '__main__':
    remove_fan_cards()
