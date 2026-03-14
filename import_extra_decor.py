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

def import_extra_decor():
    if not os.path.exists('extra_decor_products.json'):
        print("Error: extra_decor_products.json not found!")
        return

    with open('extra_decor_products.json', 'r', encoding='utf-8') as f:
        products_data = json.load(f)

    # Ensure Home & Decor category exists
    category, _ = Category.objects.get_or_create(
        name='Home & Decor',
        defaults={'description': 'Premium home and decor items for customization.'}
    )

    print(f"Starting import of {len(products_data)} extra decor products...")

    for data in products_data:
        name = data['name']
        url = data['url']
        price_str = data['price'].replace(',', '')
        try:
            import re
            match = re.search(r'\d+(\.\d+)?', price_str)
            price = float(match.group()) if match else 0.0
        except:
            price = 0.0
            
        description = data['description']
        image_url = data['image_url']
        
        if image_url.startswith('//'):
            image_url = 'https:' + image_url
        elif image_url.startswith('http://'):
            image_url = image_url.replace('http://', 'https://')

        print(f"Processing: {name}...")
        
        url_slug = url.split('/')[-1]
        
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

        filename = f"extra_decor_{url_slug}.jpg"
        try:
            print(f"  Downloading image: {image_url}")
            req = urllib.request.Request(image_url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'})
            with urllib.request.urlopen(req, timeout=15) as response:
                content = response.read()
            product.image.save(filename, ContentFile(content), save=True)
            print(f"  Successfully imported/updated {name}")
        except Exception as e:
            print(f"  Failed to download image for {name}: {e}")

    print("All extra decor products processed.")

if __name__ == '__main__':
    import_extra_decor()
