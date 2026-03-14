from django.db import models
from django.conf import settings
from products.models import Product

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, default='')
    last_name = models.CharField(max_length=50, default='')
    email = models.EmailField(default='')
    address = models.TextField()
    apartment = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100, default='')
    country = models.CharField(max_length=100, default='India')
    postal_code = models.CharField(max_length=20)
    phone = models.CharField(max_length=20, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    razorpay_order_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_payment_id = models.CharField(max_length=100, blank=True, null=True)
    PAYMENT_METHODS = [
        ('RAZORPAY', 'Card / Netbanking'),
        ('RAZORPAY_UPI', 'Razorpay UPI (GPay, PhonePe, Paytm)'),
        ('UPI_MANUAL', 'Manual UPI ID Transfer'),
        ('COD', 'Cash on Delivery (COD)'),
    ]
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS, default='RAZORPAY')
    upi_id = models.CharField(max_length=100, blank=True, null=True, help_text="Enter your UPI ID if paying via Manual UPI")

    status = models.CharField(max_length=20, default='Pending', choices=[
        ('Pending', 'Pending'),
        ('Processing', 'Processing'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
    ])
    
    # Shipping Information
    SHIPPING_PROVIDERS = [
        ('Blue Dart', 'Blue Dart'),
        ('Delhivery', 'Delhivery'),
        ('DTDC', 'DTDC'),
        ('Ecom Express', 'Ecom Express'),
        ('Amazon Shipping', 'Amazon Shipping'),
        ('Xpressbees', 'Xpressbees'),
        ('India Post', 'India Post'),
        ('Other', 'Other')
    ]
    shipping_provider = models.CharField(max_length=50, choices=SHIPPING_PROVIDERS, blank=True, null=True, help_text="Select the courier service")
    tracking_number = models.CharField(max_length=100, blank=True, null=True, help_text="Enter the AWB/Tracking number")

    def __str__(self):
        return f"Order {self.id}"

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.price * self.quantity
