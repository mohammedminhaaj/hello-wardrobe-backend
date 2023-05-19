from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .utils import ResponsePayload
from user.authentication import check_authentication
from cart_wishlist.utils import get_initial_cart_wishlist

# Create your views here.


@api_view(["POST"])
def load_initial_state(request: Request):
    authentication = check_authentication(request, get_user_id=True)
    if authentication.get("error_code") == "INVALID":
        return ResponsePayload().error(error_message="Invalid or expired token", status_code=status.HTTP_401_UNAUTHORIZED)

    initial_cart_wishlist = get_initial_cart_wishlist(
        authentication.get("is_authenticated"), authentication.get("user_id"), request.data.get("cartWishlistData", {}))
    return ResponsePayload().success(success_message="Initial data loaded successfully", data={
        "isAuthenticated": authentication.get("is_authenticated", False),
        "cart": initial_cart_wishlist.get("cart", []),
        "wishlist": initial_cart_wishlist.get("wishlist", []),
    })
