from decimal import Decimal
from django.conf import settings
from products.models import Product
from customization.models import CustomizedProduct

class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, quantity=1, override_quantity=False):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'price': str(product.price)}
        
        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def add_custom(self, design, quantity=1):
        # Unique key for customized designs
        item_id = f"design_{design.id}"
        if item_id not in self.cart:
            self.cart[item_id] = {
                'quantity': 0, 
                'price': str(design.product.price),
                'design_id': design.id
            }
        self.cart[item_id]['quantity'] += quantity
        self.save()

    def save(self):
        self.session.modified = True

    def remove(self, item_id):
        # item_id can be '123' (product) or 'design_123' (customized)
        item_id = str(item_id)
        if item_id in self.cart:
            del self.cart[item_id]
            self.save()

    def __iter__(self):
        # Separate normal products and customized designs
        normal_ids = []
        design_ids = {} # map design_id -> item_id
        
        for item_id, item_data in self.cart.items():
            if item_id.startswith('design_'):
                design_ids[item_data['design_id']] = item_id
            else:
                normal_ids.append(item_id)

        products = {str(p.id): p for p in Product.objects.filter(id__in=normal_ids)}
        designs = {d.id: d for d in CustomizedProduct.objects.filter(id__in=design_ids.keys())}
        
        cart = self.cart.copy()
        for item_id, item in cart.items():
            if item_id.startswith('design_'):
                design = designs.get(item['design_id'])
                item['product'] = design.product if design else None
                item['design'] = design
                item['id'] = item_id
            else:
                item['product'] = products.get(item_id)
                item['id'] = item_id
            
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())
    
    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()
