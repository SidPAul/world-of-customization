from django.db import models
from products.models import Product
from django.conf import settings

class CustomizedProduct(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    design_data = models.JSONField(help_text="JSON data from Fabric.js")
    preview_image = models.ImageField(upload_to='custom_designs/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Custom Design for {self.product.name} by {self.user}"
