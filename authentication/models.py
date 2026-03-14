from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('customer', 'Customer'),
        ('admin', 'Admin'),
    )
    REGION_CHOICES = (
        ('IND', 'India (₹)'),
        ('USA', 'United States ($)'),
        ('UK', 'United Kingdom (£)'),
        ('EUR', 'Europe (€)'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='customer')
    region = models.CharField(max_length=3, choices=REGION_CHOICES, default='IND')
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.username
