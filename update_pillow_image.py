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

def update_pillow_image():
    product_name = "Personalized Full-Print Pillow – Double-Sided Custom Cushion with Your Design"
    image_url = "http://colophotoshop.com/cdn/shop/files/PersonalizedFull-PrintPillow_1.jpg?v=1767534645"
    
    # Ensure https
    if image_url.startswith('http://'):
        image_url = image_url.replace('http://', 'https://')
    
    p = Product.objects.filter(name__icontains="Personalized Full-Print Pillow").first()
    
    if p:
        print(f"Updating image for: {p.name}")
        try:
            req = urllib.request.Request(image_url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'})
            with urllib.request.urlopen(req, timeout=15) as response:
                content = response.read()
            
            # Save image
            filename = "personalized_full_print_pillow.jpg"
            p.image.save(filename, ContentFile(content), save=True)
            print(f"Successfully updated image for '{p.name}'")
        except Exception as e:
            print(f"Failed to update image: {e}")
    else:
        print("Product not found")

if __name__ == '__main__':
    update_pillow_image()
