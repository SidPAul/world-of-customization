import os
import sys
import django
import urllib.request
from django.core.files.base import ContentFile

# Setup Django environment
sys.path.append(r'd:\Sem6')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from products.models import Product

FIX_MAP = {
    'Mickey Mouse Tee': 'https://images.unsplash.com/photo-1503342217505-b0a15ec3261c?q=80&w=1000',
    'Custom Photo Hoodie': 'https://images.unsplash.com/photo-1521572267360-ee0c2909d518?q=80&w=1000',
    'Custom Photo Tee': 'https://images.unsplash.com/photo-1521572267360-ee0c2909d518?q=80&w=1000',
    'ISRO Space Mug': 'https://images.unsplash.com/photo-1517210122415-b0c70b2a09bf?q=80&w=1000',
    'Handcrafted Leather Journal': 'https://images.unsplash.com/photo-1544816153-199d8a2b85a0?q=80&w=1000',
    'Metallic Minimalist Desk Organizer': 'https://images.unsplash.com/photo-1544450170-a9f218a51b67?q=80&w=1000',
    'Custom Embroidered Denim Jacket': 'https://images.unsplash.com/photo-1551537482-f2075a1d41f2?q=80&w=1000',
    'Matte Finish Phone Case': 'https://images.unsplash.com/photo-1586105251261-72a756497a11?q=80&w=1000',
    'Abstract Woven Tapestry': 'https://images.unsplash.com/photo-1582231538356-91e779a973f5?q=80&w=1000',
    'Classic Minimalist T-Shirt': 'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?q=80&w=1000',
    'Urban Oversized Hoodie': 'https://images.unsplash.com/photo-1556821840-3a63f95609a7?q=80&w=1000',
    'Velvet Touch Throw Pillow': 'https://images.unsplash.com/photo-1579656335342-fcae8b53ba21?q=80&w=1000',
    'Engraved Oak Cutting Board': 'https://images.unsplash.com/photo-1594382342004-86ca22eb620b?q=80&w=1000',
    'Leather & Felt Laptop Sleeve': 'https://images.unsplash.com/photo-1525964067082-dd193051bf9a?q=80&w=1000',
    'Gaming Precision Mouse Pad': 'https://images.unsplash.com/photo-1615663245857-ac93bb7c39e7?q=80&w=1000',
    'Eco-Friendly Canvas Tote': 'https://images.unsplash.com/photo-1544816153-199d8a2b85a0?q=80&w=1000',
    'Minimalist Wall Clock': 'https://images.unsplash.com/photo-1563861826100-9cb868fdbe1c?q=80&w=1000',
    'Premium Glass Water Bottle': 'https://images.unsplash.com/photo-1602143307185-8a155ca967ce?q=80&w=1000',
    'Cozy Knit Beanie': 'https://images.unsplash.com/photo-1576871337622-98d48d1cf027?q=80&w=1000',
    'Handmade Ceramic Coasters': 'https://images.unsplash.com/photo-1610701596007-11502861dcfa?q=80&w=1000',
    'Pro Slim Power Bank': 'https://images.unsplash.com/photo-1609091839311-d5365f9ff1c5?q=80&w=1000',
    'Illustrated Sticker Pack': 'https://images.unsplash.com/photo-1572375927501-44447e4d25a?q=80&w=1000',
    'Non-Slip Yoga Mat': 'https://images.unsplash.com/photo-1592432676556-2693bc2f754d?q=80&w=1000',
    'Custom Enamel Pin': 'https://images.unsplash.com/photo-1611681229380-45c110cd998d?q=80&w=1000'
}

def fix_images():
    for name, url in FIX_MAP.items():
        products = Product.objects.filter(name__icontains=name)
        if not products.exists():
            print(f"Product not found: {name}")
            continue
            
        for p in products:
            print(f"Fixing {p.name}...")
            filename = f"{p.name.lower().replace(' ', '_')}.jpg"
            try:
                # Add a timeout and better error handling
                req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'})
                with urllib.request.urlopen(req, timeout=10) as response:
                    content = response.read()
                    if len(content) < 1000: # Very small file might be a 404 page
                        print(f"  Warning: Small content downloaded for {p.name}, size: {len(content)}")
                p.image.save(filename, ContentFile(content), save=True)
                print(f"  Successfully fixed {p.name}")
            except Exception as e:
                print(f"  Failed to fix {p.name}: {e}")

if __name__ == '__main__':
    fix_images()
