from user.models import User
from ..models import Cart, Wishlist
from .cart import update_user_cart, get_cart_list, clean_cart_list
from .wishlist import update_user_wishlist, get_wishlist_list, clean_wishlist_list


def update_cart_wishlist(user: User, cart_wishlist_data: dict[str, list[dict[str, str]]]):

    return {
        "cart": update_user_cart(user, cart_wishlist_data.get("cart", [])),
        "wishlist": update_user_wishlist(user, cart_wishlist_data.get("wishlist", []))
    }


def get_initial_cart_wishlist(is_authenticated: bool, user_id: int | None, cart_wishlist_data: dict):

    response = {
        "cart": [],
        "wishlist": [],
    }
    if is_authenticated and user_id:
        response["cart"] = get_cart_list(
            list(Cart.objects.filter(user=User.objects.get(pk=user_id))))
        response["wishlist"] = get_wishlist_list(
            list(Wishlist.objects.filter(user=User.objects.get(pk=user_id))))

    elif cart_wishlist_data:
        cart_list = clean_cart_list(cart_wishlist_data.get("cart", []))
        wishlist_list = clean_wishlist_list(
            cart_wishlist_data.get("wishlist", []))
        response["cart"] = get_cart_list(cart_list)
        response["wishlist"] = get_wishlist_list(wishlist_list)


    return response
