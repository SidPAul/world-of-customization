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

def update_premium_wooden_plate_image():
    product_name = "Luxury Handcrafted Wooden House Name Plate"
    # Stable high-quality wooden board image from Pixabay
    image_url = "https://cdn.pixabay.com/photo/2015/07/31/15/02/wood-869230_1280.jpg"
    
    p = Product.objects.filter(name__iexact=product_name).first()
    
    if p:
        print(f"Updating image for: {p.name}")
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.get(image_url, headers=headers, timeout=20)
            if response.status_code == 200:
                # Save image
                filename = "luxury_wooden_plate_final.jpg"
                p.image.save(filename, ContentFile(response.content), save=True)
                print(f"Successfully updated image for '{p.name}'")
            else:
                print(f"Failed to download image. Status code: {response.status_code}")
        except Exception as e:
            print(f"Failed to update image: {e}")
    else:
        print(f"Product '{product_name}' not found")

if __name__ == '__main__':
    update_premium_wooden_plate_image()
