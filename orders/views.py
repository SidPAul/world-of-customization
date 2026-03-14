import razorpay
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from cart.cart import Cart
from .models import OrderItem, Order
from .forms import OrderCreateForm
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
import logging

logger = logging.getLogger(__name__)

@login_required
def order_create(request):
    cart = Cart(request)
    if len(cart) == 0:
        return redirect('product-list')

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            
            # Payment method handling
            if order.payment_method in ['RAZORPAY', 'RAZORPAY_UPI']:
                # Razorpay Integration
                payment = None
                try:
                    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
                    amount = int(cart.get_total_price() * 100) 
                    data = { "amount": amount, "currency": "INR", "receipt": str(order.id) }
                    payment = client.order.create(data=data)
                    
                    order.razorpay_order_id = payment['id']
                    order.save()
                except Exception as e:
                    logger.error(f"Razorpay Error: {str(e)}")
                    from django.contrib import messages
                    messages.warning(request, "Payment gateway issue. Order placed but payment still pending.")
                
                # We DON'T clear cart here. Only after successful payment verification.
                
                if payment:
                    context = {
                        'order': order,
                        'payment': payment,
                        'razorpay_key_id': settings.RAZORPAY_KEY_ID,
                        'is_upi': order.payment_method == 'RAZORPAY_UPI'
                    }
                    return render(request, 'orders/payment.html', context)
                else:
                    return redirect('order-history')
            
            elif order.payment_method == 'UPI_MANUAL':
                # Manual UPI payment handling
                cart.clear()
                from django.contrib import messages
                messages.success(request, f"Order placed! Please pay via Manual UPI using ID: {order.upi_id}.")
                return redirect('order-history')
                
            elif order.payment_method == 'COD':
                # Cash on Delivery handling
                cart.clear()
                from django.contrib import messages
                messages.success(request, "Order placed successfully! You can pay via Cash on Delivery.")
                return redirect('order-history')
            
            else:
                cart.clear()
                return redirect('order-history')
    else:
        form = OrderCreateForm()
    return render(request, 'orders/create.html', {'cart': cart, 'form': form})

@login_required
def order_pay(request, order_id):
    from django.contrib import messages
    order = get_object_or_404(Order, id=order_id, user=request.user, paid=False)
    
    payment = None
    try:
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        amount = int(order.get_total_cost() * 100) 
        
        # Create a new Razorpay order if none exists or fetch existing
        if not order.razorpay_order_id:
            data = { "amount": amount, "currency": "INR", "receipt": str(order.id) }
            payment = client.order.create(data=data)
            order.razorpay_order_id = payment['id']
            order.save()
        else:
            payment = client.order.fetch(order.razorpay_order_id)
            
        context = {
            'order': order,
            'payment': payment,
            'razorpay_key_id': settings.RAZORPAY_KEY_ID,
            'is_upi': order.payment_method == 'RAZORPAY_UPI'
        }
        return render(request, 'orders/payment.html', context)
    except Exception as e:
        import logging
        logging.error(f"Razorpay Fetch Error: {str(e)}")
        messages.error(request, "Failed to initialize the payment gateway. Please try again.")
        return redirect('order-history')

@csrf_exempt
@login_required
def payment_verify(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            razorpay_order_id = data.get('razorpay_order_id')
            razorpay_payment_id = data.get('razorpay_payment_id')
            razorpay_signature = data.get('razorpay_signature')

            client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
            
            # Verify signature
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': razorpay_payment_id,
                'razorpay_signature': razorpay_signature
            }
            
            client.utility.verify_payment_signature(params_dict)
            
            # Payment verified
            order = get_object_or_404(Order, razorpay_order_id=razorpay_order_id)
            order.paid = True
            order.razorpay_payment_id = razorpay_payment_id
            order.status = 'Processing'
            order.save()
            
            # Clear cart on successful payment
            cart = Cart(request)
            cart.clear()

            return JsonResponse({'status': 'success'})
        except Exception as e:
            logger.error(f"Payment Verification Failed: {str(e)}")
            return JsonResponse({'status': 'failure', 'error': str(e)}, status=400)
    
    return JsonResponse({'status': 'invalid request'}, status=400)

@login_required
def payment_success(request):
    # Fallback to clear cart if redirected here
    cart = Cart(request)
    if cart:
        cart.clear()
    return render(request, 'orders/success.html')

@login_required
def order_delete(request, order_id):
    from django.contrib import messages
    order = get_object_or_404(Order, id=order_id, user=request.user, paid=False)
    order.delete()
    messages.success(request, "Order cancelled and removed successfully.")
    return redirect('order-history')

@login_required
def order_item_delete(request, item_id):
    from django.contrib import messages
    item = get_object_or_404(OrderItem, id=item_id, order__user=request.user, order__paid=False)
    order = item.order
    
    if order.items.count() <= 1:
        order.delete()
        messages.success(request, "Order cancelled as all items were removed.")
    else:
        product_name = item.product.name
        item.delete()
        messages.success(request, f"'{product_name}' removed from your order.")
    
    return redirect('order-history')

class OrderHistoryView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'orders/order_history.html'
    context_object_name = 'orders'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by('-created_at')

class AdminOrderListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Order
    template_name = 'orders/admin_order_list.html'
    context_object_name = 'orders'

    def test_func(self):
        return self.request.user.role == 'admin'
