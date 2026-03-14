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

def update_premium_wooden_plate_image():
    product_name = "Luxury Handcrafted Wooden House Name Plate"
    # Stable high-quality wooden plaque image from Pexels
    image_url = "https://images.pexels.com/photos/3994033/pexels-photo-3994033.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1"
    
    p = Product.objects.filter(name__iexact=product_name).first()
    
    if p:
        print(f"Updating image for: {p.name}")
        try:
            req = urllib.request.Request(image_url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=15) as response:
                content = response.read()
            
            # Save image
            filename = "luxury_wooden_plate_updated.jpg"
            p.image.save(filename, ContentFile(content), save=True)
            print(f"Successfully updated image for '{p.name}'")
        except Exception as e:
            print(f"Failed to update image: {e}")
    else:
        print(f"Product '{product_name}' not found")

if __name__ == '__main__':
    update_premium_wooden_plate_image()
