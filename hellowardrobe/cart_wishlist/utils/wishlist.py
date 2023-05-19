from user.models import User
from ..models import Wishlist
from product.models import Product


def get_wishlist_response(wishlist_obj: Wishlist) -> dict[str, str]:
    return {
        "name": wishlist_obj.product.name,
        "url_name": wishlist_obj.product.url_name
    }


def get_wishlist_list(wishlist_list: list[Wishlist]) -> list[dict[str, str]]:
    return [get_wishlist_response(wishlist) for wishlist in wishlist_list]


def clean_wishlist(wishlist_data: dict[str, str], user: User):
    try:
        product = Product.objects.get(url_name=wishlist_data.get("url_name"))
        return Wishlist(
            user=user,
            product=product,
        )
    except Exception:
        return Wishlist()


def clean_and_save_wishlist(wishlist_data: dict[str, str], user: User):
    wishlist = clean_wishlist(wishlist_data, user)
    try:
        wishlist.save()
    except Exception:
        pass
    return wishlist


def clean_wishlist_list(wishlist_data: list[dict[str, str]], user: User | None = None):
    if not wishlist_data:
        return []
    if not user:
        try:
            user = User.objects.get(
                email__iexact="anonymous@hello-wardrobe.in")
        except User.DoesNotExist:
            pass
    products = Product.objects.filter(url_name__in=[
        data["url_name"] for data in wishlist_data if isinstance(data, dict) and "url_name" in data])
    return [
        Wishlist(
            user=user,
            product=product
        )
        for product in products
    ]


def update_user_wishlist(user: User, wishlist_data: list[dict[str, str]]):
    if isinstance(wishlist_data, list):
        wishlist_list = clean_wishlist_list(wishlist_data, user)
        Wishlist.objects.bulk_create(
            wishlist_list, ignore_conflicts=True) if wishlist_list else []
        wishlist_data = get_wishlist_list(
            Wishlist.objects.filter(user=user))
        return wishlist_data
    else:
        return []
