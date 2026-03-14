
import os
import django
import requests
from bs4 import BeautifulSoup
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from urllib.parse import urljoin

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from products.models import Product

def download_and_update(product_name, url, filename):
    print(f"Processing {product_name}...")
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Try to find high-res image
        img_url = None
        
        # Strategy 1: Open Graph Image
        og_image = soup.find('meta', property='og:image')
        if og_image:
            img_url = og_image['content']
            
        # Strategy 2: First main image (fallback)
        if not img_url:
            # Common patterns for product images
            img_tag = soup.find('img', {'id': 'imgBlkFront'}) # Amazon-ish
            if not img_tag:
                 img_tag = soup.find('img', class_='product-image')
            
            if img_tag:
                img_url = img_tag.get('src')
                
        if img_url:
            # Handle relative URLs
            img_url = urljoin(url, img_url)
            print(f"  Found image URL: {img_url}")
            
            img_response = requests.get(img_url, headers=headers, stream=True)
            if img_response.status_code == 200:
                # Save to a temporary file
                img_temp = NamedTemporaryFile(delete=True)
                img_temp.write(img_response.content)
                img_temp.flush()
                
                # Update product
                try:
                    product = Product.objects.get(name=product_name)
                    product.image.save(filename, File(img_temp), save=True)
                    print(f"  SUCCESS: Updated {product_name}")
                except Product.DoesNotExist:
                    print(f"  ERROR: Product {product_name} not found in DB")
            else:
                print(f"  ERROR: Could not download image from {img_url}")
        else:
            print("  ERROR: No suitable image found on page")
            
    except Exception as e:
        print(f"  Exception: {e}")

def run():
    # 1. Mickey Mouse Tee
    download_and_update(
        'Mickey Mouse Tee', 
        'https://www.ubuy.co.zw/en/product/4X2E63PI0-disney-mickey-mouse-classic-pose-short-sleeve-cotton-t-shirt-for-adults-customized-white?srsltid=AfmBOoq9VsHiPBi2TLV4vsxlIOViKBo5Z9PWW4FTpt8Lk9qtfTRzy2YT',
        'mickey_real.jpg'
    )
    
    # 2. ISRO Space Mug
    download_and_update(
        'ISRO Space Mug',
        'https://spacearcade.in/product/isro-vyomnaut-helmet-white-ceramic-coffee-mug/',
        'isro_real.jpg'
    )
    
    # 3. Custom Photo Tee (Black)
    download_and_update(
        'Custom Photo Tee',
        'https://bloomingprints.in/product/customized-black-round-neck-t-shirt/?srsltid=AfmBOoot6LxQqVC4i6k_LQ4mzlZlq_9MbKKrUZ2yNIgNYyV0-lR8gvUU',
        'black_tee_real.jpg'
    )
    
    # 4. Custom Photo Hoodie (Grey)
    download_and_update(
        'Custom Photo Hoodie',
        'https://www.temu.com/nz/customizable-photo-hoodie-cozy-gray-polyester-sweatshirt-with-kangaroo-pocket-casual-versatile--couples-machine-washable--modern--machine-washable-hoodie-g-601099971533301.html',
        'grey_hoodie_real.jpg'
    )

if __name__ == '__main__':
    run()
