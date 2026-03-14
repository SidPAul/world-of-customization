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

def import_expanded_signage():
    if not os.path.exists('nameplate_expansion_v3.json'):
        print("Error: nameplate_expansion_v3.json not found!")
        return

    with open('nameplate_expansion_v3.json', 'r', encoding='utf-8') as f:
        products_data = json.load(f)

    category, _ = Category.objects.get_or_create(
        name='Name Boards & Signage',
        defaults={'description': 'Customized office and home name boards, nameplates, and signage.'}
    )

    print(f"Starting expansion of Signage section...")

    # Real products from scraper
    target_names = [
        "LED Spotify Keychain",
        "Single Glow Name Magnet",
        "Name Frame",
        "Number Plate Keychain",
        "Tag Number Plate Keychain",
        "3D Name Keychain",
        "Couple Name Pendant",
        "Name Magnet - 12 Letters",
        "customized magnetic name badge"
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
            price = float(match.group()) if match else 199.0
            if price == 0.0: price = 199.0
        except:
            price = 199.0
            
        description = data['description']
        image_url = data['image_url']
        
        if image_url.startswith('//'):
            image_url = 'https:' + image_url
        elif image_url.startswith('http://'):
            image_url = image_url.replace('http://', 'https://')

        print(f"Processing scraped: {name}...")
        
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

        filename = f"signage_{url_slug}.jpg"
        try:
            req = urllib.request.Request(image_url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=15) as response:
                content = response.read()
            product.image.save(filename, ContentFile(content), save=True)
            print(f"  Imported {name}")
        except Exception as e:
            print(f"  Image fail for {name}: {e}")

    # Premium Synthesized Products (Unsplash)
    premium_products = [
        {
            "name": "Luxury Handcrafted Wooden House Name Plate",
            "price": 1499.0,
            "description": "Exquisite Teak wood name plate with deep-etched laser engraving. Weatherproof coating, premium gold-finish brass fixtures. Perfect for bungalow or apartment entrances.",
            "image_url": "https://images.unsplash.com/photo-1621293954908-907159247fc8?q=80&w=2070&auto=format&fit=crop",
            "slug": "premium-wooden-house-nameplate"
        },
        {
            "name": "Modern Minimalist Acrylic Door Name Plate",
            "price": 899.0,
            "description": "High-gloss dual-layer acrylic door sign with 3D raised lettering. Sleek chrome spacers included for a floating effect. Durable, UV-resistant, and contemporary design.",
            "image_url": "https://images.unsplash.com/photo-1560185007-c5ca9d2c014d?q=80&w=2070&auto=format&fit=crop",
            "slug": "modern-acrylic-door-sign"
        },
        {
            "name": "Bespoke Brass Office Nameplate with Stand",
            "price": 1250.0,
            "description": "Professional solid brass desk name plate with a heavy marble base. Perfect for executive offices and premium workspaces. Custom name and designation engraving included.",
            "image_url": "https://images.unsplash.com/photo-1497215728101-856f4ea42174?q=80&w=2070&auto=format&fit=crop",
            "slug": "bespoke-brass-office-nameplate"
        }
    ]

    for p_data in premium_products:
        print(f"Adding Premium: {p_data['name']}...")
        product, created = Product.objects.get_or_create(
            name=p_data['name'],
            defaults={
                'category': category,
                'description': p_data['description'],
                'price': p_data['price'],
                'stock': 50,
                'is_customizable': True
            }
        )
        try:
            req = urllib.request.Request(p_data['image_url'], headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=15) as response:
                content = response.read()
            product.image.save(f"{p_data['slug']}.jpg", ContentFile(content), save=True)
            print(f"  Added premium {p_data['name']}")
        except Exception as e:
            print(f"  Premium image fail: {e}")

    print("Signage expansion complete.")

if __name__ == '__main__':
    import_expanded_signage()
