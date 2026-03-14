import json
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from products.models import Product
from .models import CustomizedProduct
from django.core.files.base import ContentFile
import base64

def customizer_view(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'customization/customizer.html', {'product': product})

from cart.cart import Cart

def save_design(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            product_id = data.get('product_id')
            design_json = data.get('design_data')
            image_data = data.get('preview_image')

            if not image_data:
                return JsonResponse({'status': 'error', 'message': 'No preview image provided'}, status=400)

            # Decode base64 image
            try:
                format, imgstr = image_data.split(';base64,') 
                ext = format.split('/')[-1] 
                data_img = ContentFile(base64.b64decode(imgstr), name=f'design_{product_id}.{ext}')
            except Exception as e:
                return JsonResponse({'status': 'error', 'message': f'Image decoding failed: {str(e)}'}, status=400)

            product = get_object_or_404(Product, pk=product_id)
            
            # Ensure design_data is a dict/list for JSONField
            if isinstance(design_json, str):
                try:
                    design_json = json.loads(design_json)
                except:
                    pass

            custom_design = CustomizedProduct.objects.create(
                user=request.user if request.user.is_authenticated else None,
                product=product,
                design_data=design_json,
                preview_image=data_img
            )
            
            # Add to Cart
            cart = Cart(request)
            cart.add_custom(custom_design)
            
            return JsonResponse({'status': 'success', 'design_id': custom_design.id})
        except Exception as e:
            import traceback
            print(traceback.format_exc())
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)
