from django.urls import path
from product import views

urlpatterns = [
    path('all-products/filter', views.list_products, name='products'),
    path('filter-details/', views.filter_details, name='filter-details'),
    path('<slug:url_name>/', views.product_overview, name='product-overview'),
]