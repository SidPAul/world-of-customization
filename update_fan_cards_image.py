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

def update_fan_cards_image():
    product_name = "Fan cards"
    # New image found on the product page (BTS themed)
    image_url = "https://moderngifts.in/cdn/shop/files/bts.webp?v=1740293164&width=1946"
    
    p = Product.objects.filter(name__iexact=product_name).first()
    if not p:
        p = Product.objects.filter(name__icontains="Fan cards").first()
    
    if p:
        print(f"Updating image for: {p.name}")
        try:
            req = urllib.request.Request(image_url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'})
            with urllib.request.urlopen(req, timeout=15) as response:
                content = response.read()
            
            # Save image
            filename = "fan_cards_new.webp"
            p.image.save(filename, ContentFile(content), save=True)
            print(f"Successfully updated image for '{p.name}'")
        except Exception as e:
            print(f"Failed to update image: {e}")
    else:
        print("Product 'Fan cards' not found")

if __name__ == '__main__':
    update_fan_cards_image()
