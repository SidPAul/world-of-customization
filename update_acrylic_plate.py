import os
import sys
import django
import requests
from django.core.files.base import ContentFile

# Setup Django environment
sys.path.append(r'd:\Sem6')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from products.models import Product

def update_acrylic_plate_image():
    product_name = "Modern Minimalist Acrylic Door Name Plate"
    # Stable high-quality acrylic visual from the primary source
    image_url = "https://moderngifts.in/cdn/shop/files/a3.webp?v=1744000893"
    
    p = Product.objects.filter(name__iexact=product_name).first()
    
    if p:
        print(f"Updating image for: {p.name}")
        try:
            # Using robust headers
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.get(image_url, headers=headers, timeout=20)
            if response.status_code == 200:
                # Save image
                filename = "modern_acrylic_plate_updated.jpg"
                p.image.save(filename, ContentFile(response.content), save=True)
                print(f"Successfully updated image for '{p.name}'")
            else:
                print(f"Failed to download image. Status: {response.status_code}")
        except Exception as e:
            print(f"Failed to update image: {e}")
    else:
        print(f"Product '{product_name}' not found")

if __name__ == '__main__':
    update_acrylic_plate_image()
