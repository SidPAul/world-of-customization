from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'created_at', 'status', 'payment_method', 'paid', 'shipping_provider', 'tracking_number']
    list_filter = ['status', 'payment_method', 'paid', 'created_at']
    search_fields = ['first_name', 'last_name', 'email', 'tracking_number', 'upi_id']
    list_editable = ['status', 'paid', 'shipping_provider', 'tracking_number']
    inlines = [OrderItemInline]
    
    fieldsets = (
        ('User & Contact', {
            'fields': ('user', 'first_name', 'last_name', 'email', 'phone')
        }),
        ('Address', {
            'fields': ('address', 'apartment', 'city', 'state', 'country', 'postal_code')
        }),
        ('Payment', {
            'fields': ('payment_method', 'upi_id', 'paid', 'razorpay_order_id', 'razorpay_payment_id')
        }),
        ('Status & Shipping', {
            'fields': ('status', 'shipping_provider', 'tracking_number'),
            'description': 'Update the status to Shipped and enter tracking details below to notify the customer.'
        }),
    )
