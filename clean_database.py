import os
import sys
import django
import shutil

# Setup Django environment
sys.path.append(r'd:\Sem6')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from products.models import Product, Category
from customization.models import CustomizedProduct
from orders.models import Order, OrderItem

def clean_database():
    print("Starting database cleanup...")

    # 1. Delete all Customized Products (including images)
    print("Deleting CustomizedProducts...")
    for cp in CustomizedProduct.objects.all():
        if cp.preview_image:
            if os.path.isfile(cp.preview_image.path):
                os.remove(cp.preview_image.path)
        cp.delete()

    # 2. Delete all Orders (this will cascade to OrderItems)
    print("Deleting Orders and OrderItems...")
    Order.objects.all().delete()

    # 3. Delete all Products (including images)
    print("Deleting Products...")
    for p in Product.objects.all():
        if p.image:
            if os.path.isfile(p.image.path):
                os.remove(p.image.path)
        p.delete()

    # 4. Delete all Categories (including images)
    print("Deleting Categories...")
    for c in Category.objects.all():
        if c.image:
            if os.path.isfile(c.image.path):
                os.remove(c.image.path)
        c.delete()

    # 5. Optional: Clean media directories if they still exist
    media_products = r'd:\Sem6\media\products'
    media_categories = r'd:\Sem6\media\categories'
    media_custom = r'd:\Sem6\media\custom_designs'

    for path in [media_products, media_categories, media_custom]:
        if os.path.exists(path):
            print(f"Cleaning directory: {path}")
            for filename in os.listdir(path):
                file_path = os.path.join(path, filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as e:
                    print(f'Failed to delete {file_path}. Reason: {e}')

    print("Cleanup complete. Database is now empty of products, categories, orders, and custom designs.")

if __name__ == '__main__':
    clean_database()
