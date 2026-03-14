import os
import sys
import django
import json
import urllib.request
import re
from django.core.files.base import ContentFile

# Setup Django environment
sys.path.append(r'd:\Sem6')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from products.models import Category, Product

def clean_price(price_str):
    if not price_str:
        return 0.0
    if isinstance(price_str, (int, float)):
        return float(price_str)
    
    price_str = price_str.replace(',', '')
    match = re.search(r'\d+(\.\d+)?', price_str)
    if match:
        return float(match.group())
    return 0.0

def get_category_name(name, url):
    name_lower = name.strip().lower()
    url_lower = url.strip().lower()
    
    if any(k in name_lower or k in url_lower for k in ['mug', 'cup', 'bottle', 'tumbler', 'tiffin', 'beer']):
        return 'Mugs & Drinkware'
    if any(k in name_lower or k in url_lower for k in ['frame', 'plaque', 'panel', 'canvas', 'collage', 'photo stand', 'scan frame']):
        return 'Photo Frames'
    if any(k in name_lower or k in url_lower for k in ['t-shirt', 'tee', 'cap', 'hoodie', 'bracelet', 'band', 'jewellery', 'pendant']):
        return 'Personalized Accessories'
    if any(k in name_lower or k in url_lower for k in ['keychain', 'bag tag', 'magnet', 'bottle of', 'pouch']):
        return 'Accessories & Keepsakes'
    if any(k in name_lower or k in url_lower for k in ['pillow', 'cushion', 'mat', 'coaster', 'tree', 'moon', 'star', 'calendar', 'stand']):
        return 'Home & Decor'
    if any(k in name_lower or k in url_lower for k in ['diary', 'pen', 'stationery', 'pencil', 'pouch']):
        return 'Stationery'
    if any(k in name_lower or k in url_lower for k in ['cards', 'game', 'puzzle', 'cone']):
        return 'Games & Fun'
    if any(k in name_lower or k in url_lower for k in ['box', 'set', 'combo', 'gift']):
        return 'Gift Sets'
    
    return 'Miscellaneous'

def import_modern_products():
    if not os.path.exists('modern_products.json'):
        print("Error: modern_products.json not found!")
        return

    with open('modern_products.json', 'r', encoding='utf-8') as f:
        products_data = json.load(f)

    print(f"Starting import of {len(products_data)} modern products...")

    for data in products_data:
        name = data['name']
        url = data['url']
        cat_name = get_category_name(name, url)
        
        category, _ = Category.objects.get_or_create(
            name=cat_name,
            defaults={'description': f'Premium {cat_name.lower()} for customization.'}
        )

        price = clean_price(data['price'])
        description = data['description']
        image_url = data['image_url']
        
        if image_url.startswith('//'):
            image_url = 'https:' + image_url
        elif image_url.startswith('http://'):
            image_url = image_url.replace('http://', 'https://')

        print(f"Processing: {name} ({cat_name})...")
        
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

        filename = f"modern_{url_slug}.jpg"
        try:
            print(f"  Downloading image: {image_url}")
            req = urllib.request.Request(image_url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'})
            with urllib.request.urlopen(req, timeout=15) as response:
                content = response.read()
            product.image.save(filename, ContentFile(content), save=True)
            print(f"  Successfully imported/updated {name}")
        except Exception as e:
            print(f"  Failed to download image for {name}: {e}")

    print("All modern products processed.")

if __name__ == '__main__':
    import_modern_products()
