from rest_framework.request import Request
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from user.authentication import CustomJWTAuthentication
from rest_framework.permissions import IsAuthenticated
from common.utils import ResponsePayload
from .utils import clean_and_save_cart, clean_and_save_wishlist, clean_cart, clean_wishlist
from .models import Cart, Wishlist
from rest_framework import status


# Create your views here.
@api_view(["POST"])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def add_to_cart(request: Request):
    clean_and_save_cart(request.data, request.user)
    return ResponsePayload().success()


@api_view(["POST"])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def remove_from_cart(request: Request):
    try:
        url_name = request.data.get("url_name")
        size = request.data.get("size")
        cart = Cart.objects.get(user=request.user, product__url_name=url_name if isinstance(
            url_name, str) else None, size__size__display_name=size if isinstance(size, str) else None)
        cart.delete()
        return ResponsePayload().success()
    except (Cart.DoesNotExist, Cart.MultipleObjectsReturned):
        return ResponsePayload().error(status_code=status.HTTP_404_NOT_FOUND)


@api_view(["POST"])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def add_to_wishlist(request: Request):
    clean_and_save_wishlist(request.data, request.user)
    return ResponsePayload().success()


@api_view(["POST"])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def remove_from_wishlist(request: Request):
    try:
        url_name = request.data.get("url_name")
        wishlist = Wishlist.objects.get(user = request.user, product__url_name = url_name if isinstance(url_name, str) else None)
        wishlist.delete()
        return ResponsePayload().success()
    except (Wishlist.DoesNotExist, Wishlist.MultipleObjectsReturned):
        return ResponsePayload().error(status_code=status.HTTP_404_NOT_FOUND)
