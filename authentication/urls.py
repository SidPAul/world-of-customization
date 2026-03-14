from django.urls import path
from .views import RegisterView, CustomLoginView, CustomLogoutView, ProfileView, firebase_login

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('firebase-login/', firebase_login, name='firebase-login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
]
