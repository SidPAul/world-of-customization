from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'phone_number', 'address', 'region')
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
        }

class CustomLoginForm(AuthenticationForm):
    pass
