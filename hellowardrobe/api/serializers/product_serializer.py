from rest_framework import serializers
from product.models import Product

class ProductSerializer(serializers.ModelSerializer):
    primary_category_name = serializers.CharField(source='primary_category.name')
    secondary_category_name = serializers.CharField(source='secondary_category.name')
    
    class Meta: 
        model = Product
        fields = ['id','name','price','primary_category_name','secondary_category_name']