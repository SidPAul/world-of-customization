from django.urls import path
from . import views

urlpatterns = [
    path('design/<int:product_id>/', views.customizer_view, name='customizer'),
    path('save/', views.save_design, name='save-design'),
]
