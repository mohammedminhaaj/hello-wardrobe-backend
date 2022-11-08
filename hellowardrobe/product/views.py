from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Product, Tag, Size
from api.serializers.product_serializer import ProductSerializer, TagSerializer, SizeSerializer


# Create your views here.

@api_view(['GET'])
def list_products(request):
    products = Product.objects.select_related('primary_category', 'secondary_category').prefetch_related(
        'size', 'tags').filter(is_active=True).defer('created_on', 'updated_on', 'is_active')
    if request.GET.getlist('size'):
        products = products.filter(size__name__in=request.GET.getlist('size'))
    if request.GET.getlist('occasion'):
        products = products.filter(
            tags__name__in=request.GET.getlist('occasion'))
    if request.GET.getlist('color'):
        products = products.filter(tags__name__in=request.GET.getlist('color'))
    if request.GET.getlist('type'):
        products = products.filter(tags__name__in=request.GET.getlist('type'))
    serializer = ProductSerializer(products.distinct(), many=True)
    return Response(serializer.data)


@api_view(['GET'])
def filter_details(request):
    filter_data = Tag.objects.filter(is_active=True)
    size_data = Size.objects.filter(is_active=True)
    filter_data_serializer = TagSerializer(filter_data, many=True)
    size_data_serializer = SizeSerializer(size_data, many=True)
    response = {
        'filter_details': filter_data_serializer.data,
        'size_details': size_data_serializer.data
    }
    return Response(response)
