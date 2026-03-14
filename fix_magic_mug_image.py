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

def fix_magic_mug_image():
    product_name = 'Magical Custom Mug – The Mug That Reveals Your Memories!'
    try:
        product = Product.objects.get(name=product_name)
        # Using a black ceramic mug image to represent the magic mug
        image_url = 'https://images.unsplash.com/photo-1517256011271-bf5f54327299?auto=format&fit=crop&q=80&w=800'
        
        print(f'Downloading correct black ceramic mug image from {image_url}...')
        req = urllib.request.Request(image_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            content = response.read()
            
        product.image.save('magic_mug_fixed.jpg', ContentFile(content), save=True)
        print(f'Successfully fixed image for product: {product.name}')
    except Product.DoesNotExist:
        print(f'Error: Product "{product_name}" not found.')
    except Exception as e:
        print(f'Error: {e}')

if __name__ == '__main__':
    fix_magic_mug_image()
