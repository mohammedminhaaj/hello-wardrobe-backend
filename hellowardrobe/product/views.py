from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from .models import Product, Tag, Size, PrimaryCategory, SecondaryCategory, TagMaster, SortMenu
from api.serializers.product_serializer import ProductListSerializer, ProductOverviewSerializer, FilterSerializer
from common.utils import ResponsePayload


# Create your views here.

@api_view(['GET'])
def list_products(request: Request):
    paginator = PageNumberPagination()
    paginator.page_size = 30
    applied_filter_dictionary = {
        'primary': 'primary_category__display_name__in',
        'secondary': 'secondary_category__display_name__in',
        'size': 'size__display_name__in',
        'occasion': 'tags__display_name__in',
        'color': 'tags__display_name__in',
        'type': 'tags__display_name__in',
    }

    filter_dict = {}

    for value in request.query_params:
        if applied_filter_dictionary.get(value.lower()) not in filter_dict:
            filter_dict[applied_filter_dictionary.get(
                value.lower())] = request.query_params.getlist(value)
        else:
            filter_dict[applied_filter_dictionary.get(
                value.lower())].extend(request.query_params.getlist(value))

    if None in filter_dict:
        del filter_dict[None]

    products = Product.objects.filter(**filter_dict)

    if request.query_params.getlist('sort'):
        products = products.order_by(request.query_params.get('sort'))

    products = products.distinct()

    result = paginator.paginate_queryset(products, request)
    serializer = ProductListSerializer(result, many=True)
    return paginator.get_paginated_response(serializer.data)


@api_view(['GET'])
def filter_details(request):
    primary_category_data = PrimaryCategory.objects.all()
    secondary_category_data = SecondaryCategory.objects.all()
    size_data = Size.objects.all()
    filter_labels = TagMaster.objects.all()
    filter_data = Tag.objects.select_related('category').all()
    sort_menu = SortMenu.objects.all()

    filter_dict = {
        'primary_category_details': primary_category_data,
        'secondary_category_details': secondary_category_data,
        'size_details': size_data,
        'filter_labels': filter_labels,
        'filter_details': filter_data,
        "sort_menu": sort_menu
    }

    serializer = FilterSerializer(filter_dict)
    return ResponsePayload().success(data=serializer.data)


@api_view(['GET'])
def product_overview(request, url_name):
    try:
        product = Product.all_objects.defer(
            'primary_category', 'secondary_category', 'tags', 'created_at', 'deleted_by', 'modified_at', 'created_by', 'modified_by').get(url_name=url_name)
        serializer = ProductOverviewSerializer(product, many=False)
        return ResponsePayload().success(data=serializer.data)
    except Product.DoesNotExist:
        return ResponsePayload().error("We couldn't find the product which you're looking for", status.HTTP_404_NOT_FOUND)
