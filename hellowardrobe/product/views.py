from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Product
from api.serializers.product_serializer import ProductSerializer


# Create your views here.
@api_view(['GET'])
def all_products(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many = True)
    return Response(serializer.data)
