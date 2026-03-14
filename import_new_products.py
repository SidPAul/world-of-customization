import os
import sys
import django
import json
import urllib.request
from django.core.files.base import ContentFile

# Setup Django environment
sys.path.append(r'd:\Sem6')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from products.models import Category, Product

def import_new_products():
    json_path = os.path.join(os.path.dirname(__file__), 'more_products.json')
    with open(json_path, 'r') as f:
        products_data = json.load(f)

    for data in products_data:
        cat_name = data['category']
        
        category, _ = Category.objects.get_or_create(
            name=cat_name,
            defaults={'description': f'Premium {cat_name.lower()} for customization.'}
        )

        name = data['name']
        price = data['price']
        description = data['description']
        image_url = data['image_url']
        
        print(f"Processing: {name} ({cat_name})...")
        
        product, created = Product.objects.update_or_create(
            name=name,
            defaults={
                'category': category,
                'description': description,
                'price': price,
                'stock': 100,
                'is_customizable': True
            }
        )

        # Download and update image
        filename = f"{name.lower().replace(' ', '_')}.jpg"
        try:
            print(f"  Downloading image: {image_url}")
            req = urllib.request.Request(image_url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as response:
                content = response.read()
            product.image.save(filename, ContentFile(content), save=True)
            print(f"  Successfully updated {name}")
        except Exception as e:
            print(f"  Failed to download image for {name}: {e}")

if __name__ == '__main__':
    import_new_products()
