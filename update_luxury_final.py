import os
import sys
import django
import requests

# Setup Django environment
sys.path.append(r'd:\Sem6')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from products.models import Product
from django.core.files.base import ContentFile

def update_luxury_image_final():
    product_name = "Luxury Handcrafted Wooden House Name Plate"
    # A high-quality name stand image from the primary source site
    image_url = "https://moderngifts.in/cdn/shop/files/3-6.webp?v=1738574582"
    
    p = Product.objects.filter(name__iexact=product_name).first()
    
    if p:
        print(f"Updating image for: {p.name}")
        try:
            # We know moderngifts.in works based on previous successful imports
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(image_url, headers=headers, timeout=15)
            if response.status_code == 200:
                filename = "luxury_wooden_plate_updated_v2.webp"
                p.image.save(filename, ContentFile(response.content), save=True)
                print(f"Successfully updated image for '{p.name}'")
            else:
                print(f"Failed to download image. Status: {response.status_code}")
        except Exception as e:
            print(f"Failed: {e}")
    else:
        print(f"Product not found")

if __name__ == '__main__':
    update_luxury_image_final()
