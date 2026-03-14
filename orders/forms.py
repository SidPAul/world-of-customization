from django import forms
from .models import Order

class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'address', 'apartment', 'city', 'state', 'country', 'postal_code', 'phone', 'payment_method', 'upi_id']
