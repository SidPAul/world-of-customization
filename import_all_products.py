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
    # Handle both string price and already cleaned numeric price
    if isinstance(price_str, (int, float)):
        return float(price_str)
    
    # Extract number from "Rs. 199.00" or "1,199.00" or "429"
    # Remove commas first
    price_str = price_str.replace(',', '')
    match = re.search(r'\d+(\.\d+)?', price_str)
    if match:
        return float(match.group())
    return 0.0

def get_category_name(name, url):
    name_lower = name.lower()
    url_lower = url.lower()
    
    if any(k in name_lower or k in url_lower for k in ['mug', 'cup', 'tumbler', 'tiffin']):
        return 'Mugs & Drinkware'
    if any(k in name_lower or k in url_lower for k in ['frame', 'plaque', 'panel', 'canvas']):
        return 'Photo Frames'
    if any(k in name_lower or k in url_lower for k in ['t-shirt', 'tee', 'cap', 'hoodie', 'apparel']):
        return 'Apparel'
    if any(k in name_lower or k in url_lower for k in ['keychain', 'bag tag', 'magnet', 'pouch', 'band', 'pendant']):
        return 'Personalized Accessories'
    if any(k in name_lower or k in url_lower for k in ['pillow', 'cushion', 'mat', 'coaster']):
        return 'Home Decor'
    if any(k in name_lower or k in url_lower for k in ['diary', 'pen', 'stationery', 'pencil']):
        return 'Stationery'
    if any(k in name_lower or k in url_lower for k in ['cards', 'game']):
        return 'Games & Fun'
    if any(k in name_lower or k in url_lower for k in ['box', 'set', 'combo', 'gift']):
        return 'Gift Sets'
    
    return 'Miscellaneous'

def import_products():
    if not os.path.exists('products_data.json'):
        print("Error: products_data.json not found!")
        return

    with open('products_data.json', 'r') as f:
        products_data = json.load(f)

    print(f"Starting import of {len(products_data)} products...")

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
        
        # Some URLs might be missing protocol or use http
        if image_url.startswith('//'):
            image_url = 'https:' + image_url
        elif image_url.startswith('http://'):
            image_url = image_url.replace('http://', 'https://')

        print(f"Processing: {name} ({cat_name})...")
        
        # Use slug from URL for filename to avoid duplicate names issue
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

        # Download and update image
        filename = f"{url_slug}.jpg"
        try:
            print(f"  Downloading image: {image_url}")
            req = urllib.request.Request(image_url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'})
            with urllib.request.urlopen(req, timeout=15) as response:
                content = response.read()
            product.image.save(filename, ContentFile(content), save=True)
            print(f"  Successfully imported/updated {name}")
        except Exception as e:
            print(f"  Failed to download image for {name}: {e}")

    print("All products processed.")

if __name__ == '__main__':
    import_products()
