from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView, TemplateView
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import CustomUserCreationForm, CustomLoginForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .firebase_utils import verify_token
from django.contrib.auth import get_user_model

User = get_user_model()

class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'authentication/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        messages.success(self.request, "Registration successful! Please login.")
        return super().form_valid(form)

class CustomLoginView(LoginView):
    authentication_form = CustomLoginForm
    template_name = 'authentication/login.html'
    
    def get_success_url(self):
        user = self.request.user
        if user.role == 'admin':
            return reverse_lazy('admin-dashboard')
        return reverse_lazy('product-list')

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('home')

class ProfileView(TemplateView):
    template_name = 'authentication/profile.html'

@csrf_exempt
def firebase_login(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            token = data.get('idToken')
            decoded_token = verify_token(token)
            
            if decoded_token:
                uid = decoded_token.get('uid')
                email = decoded_token.get('email')
                name = decoded_token.get('name', '')
                
                # Get or create user
                user, created = User.objects.get_or_create(username=email, defaults={
                    'email': email,
                    'first_name': name,
                })
                
                login(request, user)
                
                return JsonResponse({'status': 'success', 'redirect_url': '/'})
            else:
                return JsonResponse({'status': 'error', 'message': 'Invalid token'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)
