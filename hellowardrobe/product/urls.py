from django.urls import path
from product import views

urlpatterns = [
    path('all-products/', views.all_products, name='all-products'),
]