from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from .models import Product, Tag, Size, PrimaryCategory, SecondaryCategory, TagMaster
from api.serializers.product_serializer import ProductListSerializer, ProductOverviewSerializer, TagSerializer, SizeSerializer, PrimaryCategorySerializer, SecondaryCategorySerializer, TagMasterSerializer


# Create your views here.

@api_view(['GET'])
def list_products(request):
    paginator = PageNumberPagination()
    paginator.page_size = 30

    products = Product.objects.select_related('primary_category', 'secondary_category').prefetch_related(
        'size', 'tags').filter(is_active=True)

    if request.GET.getlist('primary'):
        products = products.filter(
            primary_category__name__in=request.GET.getlist('primary'))
    if request.GET.getlist('secondary'):
        products = products.filter(
            secondary_category__name__in=request.GET.getlist('secondary'))
    if request.GET.getlist('size'):
        products = products.filter(size__name__in=request.GET.getlist('size'))
    if request.GET.getlist('occasion'):
        products = products.filter(
            tags__name__in=request.GET.getlist('occasion'))
    if request.GET.getlist('color'):
        products = products.filter(tags__name__in=request.GET.getlist('color'))
    if request.GET.getlist('type'):
        products = products.filter(tags__name__in=request.GET.getlist('type'))
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

    primary_category_serializer = PrimaryCategorySerializer(
        primary_category_data, many=True)
    secondary_category_serializer = SecondaryCategorySerializer(
        secondary_category_data, many=True)
    size_data_serializer = SizeSerializer(size_data, many=True)
    filter_label_serializer = TagMasterSerializer(filter_labels, many=True)
    filter_data_serializer = TagSerializer(filter_data, many=True)

    response = {
        'primary_category_details': primary_category_serializer.data,
        'secondary_category_details': secondary_category_serializer.data,
        'size_details': size_data_serializer.data,
        'filter_labels': filter_label_serializer.data,
        'filter_details': filter_data_serializer.data,
    }
    return Response(response)


@api_view(['GET'])
def product_overview(request, url_name):
    product = Product.objects.get(url_name=url_name)
    serializer = ProductOverviewSerializer(product, many=False)
    return Response(serializer.data)
