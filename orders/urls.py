from django.urls import path
from . import views

urlpatterns = [
    path('checkout/', views.order_create, name='checkout'),
    path('pay/<int:order_id>/', views.order_pay, name='order-pay'),
    path('success/', views.payment_success, name='payment-success'),
    path('history/', views.OrderHistoryView.as_view(), name='order-history'),
    path('delete/<int:order_id>/', views.order_delete, name='order-delete'),
    path('item/delete/<int:item_id>/', views.order_item_delete, name='order-item-delete'),
    path('manage/', views.AdminOrderListView.as_view(), name='admin-order-list'),
]
