from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from .models import Product, Tag, Size, PrimaryCategory, SecondaryCategory, TagMaster
from api.serializers.product_serializer import ProductListSerializer, ProductOverviewSerializer, FilterSerializer


# Create your views here.

@api_view(['GET'])
def list_products(request: Request):
    paginator = PageNumberPagination()
    paginator.page_size = 30
    applied_filter_dictionary = {
        'primary': 'primary_category__name__in',
        'secondary': 'secondary_category__name__in',
        'size': 'size__name__in',
        'occasion': 'tags__name__in',
        'color': 'tags__name__in',
        'type': 'tags__name__in',
    }
    filter_dict = {}

    products = Product.objects.select_related('primary_category', 'secondary_category').prefetch_related(
        'size', 'tags').filter(is_active=True)

    for value in request.GET:
        if applied_filter_dictionary.get(value) not in filter_dict:
            filter_dict[applied_filter_dictionary.get(
                value)] = request.GET.getlist(value)
        else:
            filter_dict[applied_filter_dictionary.get(
                value)].extend(request.GET.getlist(value))

    if None in filter_dict:
        del filter_dict[None]

    products = products.filter(**filter_dict)

    if request.GET.getlist('sort'):
        products = products.order_by(request.GET.get('sort'))

    products = products.only(
        'name', 'price', 'primary_category', 'secondary_category').distinct()
        
    result = paginator.paginate_queryset(products, request)
    serializer = ProductListSerializer(result, many=True)
    return paginator.get_paginated_response(serializer.data)


@api_view(['GET'])
def filter_details(request):
    primary_category_data = PrimaryCategory.objects.filter(is_active=True)
    secondary_category_data = SecondaryCategory.objects.filter(is_active=True)
    size_data = Size.objects.filter(is_active=True)
    filter_labels = TagMaster.objects.filter(is_active=True)
    filter_data = Tag.objects.select_related('category').filter(is_active=True)

    filter_sidebar_dict = {
        'primary_category_details': primary_category_data,
        'secondary_category_details': secondary_category_data,
        'size_details': size_data,
        'filter_labels': filter_labels,
        'filter_details': filter_data,
    }

    serializer = FilterSerializer(filter_sidebar_dict)

    return Response(serializer.data)


@api_view(['GET'])
def product_overview(request, url_name):
    try:
        product = Product.objects.defer(
            'primary_category', 'secondary_category', 'tags', 'created_on', 'updated_on').get(url_name=url_name)
        serializer = ProductOverviewSerializer(product, many=False)
        return Response(serializer.data)
    except Product.DoesNotExist:
        return Response({"message": 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
