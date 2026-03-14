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

def import_nameplates():
    if not os.path.exists('nameplate_potential.json'):
        print("Error: nameplate_potential.json not found!")
        return

    with open('nameplate_potential.json', 'r', encoding='utf-8') as f:
        products_data = json.load(f)

    # Ensure "Name Boards & Signage" category exists
    category, _ = Category.objects.get_or_create(
        name='Name Boards & Signage',
        defaults={'description': 'Customized office and home name boards, nameplates, and signage.'}
    )

    print(f"Starting import of name plate style products...")

    # Filter for specific products we want to add to this section
    target_names = [
        "Spotify Acrylic Photo Stand",
        "Graduation Stand",
        "Acrylic Star Stand",
        "Acrylic Moon Stand",
        "Name Pen Stand",
        "Customized Acrylic Logo Stand",
        "Baby Photo stand",
        "Acrylic Photo Frame A4",
        "Mini Love Wooden Photo Frame"
    ]

    for data in products_data:
        name = data['name']
        if not any(target.lower() in name.lower() for target in target_names):
            continue
            
        url = data['url']
        price_str = data['price'].replace(',', '')
        try:
            import re
            match = re.search(r'\d+(\.\d+)?', price_str)
            price = float(match.group()) if match else 299.0 # Default price if zero/missing
            if price == 0.0: price = 299.0
        except:
            price = 299.0
            
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

        filename = f"nameplate_{url_slug}.jpg"
        try:
            print(f"  Downloading image: {image_url}")
            req = urllib.request.Request(image_url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'})
            with urllib.request.urlopen(req, timeout=15) as response:
                content = response.read()
            product.image.save(filename, ContentFile(content), save=True)
            print(f"  Successfully imported/updated {name}")
        except Exception as e:
            print(f"  Failed to download image for {name}: {e}")

    print("Name plate expansion complete.")

if __name__ == '__main__':
    import_nameplates()
