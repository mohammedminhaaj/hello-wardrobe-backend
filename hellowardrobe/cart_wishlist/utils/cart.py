from user.models import User
from ..models import Cart, TimeMaster
from product.models import Product, ProductSize
from datetime import date, datetime
from common import constants


def validate_date(date_obj: str) -> date | None:
    try:
        return datetime.strptime(date_obj, constants.COMMON_DATE_FORMAT).date()
    except Exception:
        return None


def get_rent_days(start_date: date, end_date: date) -> int:
    delta = end_date - start_date
    return delta.days + 1


def get_cart_response(cart_obj: Cart) -> dict[str, str]:
    return {
        "startDate": cart_obj.from_date.strftime(constants.COMMON_DATE_FORMAT),
        "endDate": cart_obj.to_date.strftime(constants.COMMON_DATE_FORMAT),
        "price": cart_obj.product.price,
        "name": cart_obj.product.name,
        "deliverAt": cart_obj.deliver_at.display_name,
        "returnBy": cart_obj.return_by.display_name,
        "size": cart_obj.size.size.display_name,
        "url_name": cart_obj.product.url_name,
        "rentDays": get_rent_days(cart_obj.from_date, cart_obj.to_date)
    }


def clean_cart(cart_data: dict[str, str], user: User):
    try:
        product = Product.objects.get(url_name=cart_data.get("url_name"))
        time_masters = TimeMaster.objects.filter(
            display_name__in=[cart_data.get("deliverAt"), cart_data.get("returnBy")])
        time_master_lookup = {
            time_master.display_name: time_master for time_master in time_masters}
        product_size = ProductSize.objects.get(
            product=product, size__display_name=cart_data.get("size"))
        return Cart(
            user=user,
            product=product,
            from_date=validate_date(cart_data.get("startDate")),
            deliver_at=time_master_lookup.get(cart_data.get("deliverAt")),
            to_date=validate_date(cart_data.get("endDate")),
            return_by=time_master_lookup.get(cart_data.get("returnBy")),
            size=product_size
        )
    except Exception:
        return Cart()


def clean_and_save_cart(cart_data: dict[str, str], user: User):
    cart = clean_cart(cart_data, user)
    try:
        cart.save()
    except Exception:
        pass
    return cart


def get_cart_list(cart_list: list[Cart]) -> list[dict[str, str | int | float]]:
    return [get_cart_response(cart) for cart in cart_list]


def clean_cart_list(cart_data: list[dict[str, str]], user: User | None = None):

    if not cart_data:
        return []

    if not user:
        try:
            user = User.objects.get(
                email__iexact="anonymous@hello-wardrobe.in")
        except User.DoesNotExist:
            pass

    products = Product.objects.filter(
        url_name__in=[data["url_name"] for data in cart_data if isinstance(
            data, dict) and "url_name" in data and isinstance(data["url_name"], str)]
    )
    sizes = ProductSize.objects.select_related("size").filter(
        size__display_name__in=[data["size"] for data in cart_data if isinstance(
            data, dict) and "size" in data and isinstance(data["size"], str)],
        product__in=products
    )
    time_masters = TimeMaster.objects.filter(
        display_name__in=[
            data[key]
            for data in cart_data
            if isinstance(data, dict)
            for key in ["deliverAt", "returnBy"]
            if key in data and isinstance(data[key], str)
        ]
    )

    product_lookup = {product.url_name: product for product in products}
    size_lookup = {
        product_size.product_size_key: product_size for product_size in sizes}
    time_master_lookup = {
        time_master.display_name: time_master for time_master in time_masters}

    kwargs_list = [
        {
            "user": user,
            "product": product_lookup.get(data.get("url_name")),
            "from_date": validate_date(data.get("startDate")),
            "deliver_at": time_master_lookup.get(data.get("deliverAt")),
            "to_date": validate_date(data.get("endDate")),
            "return_by": time_master_lookup.get(data.get("returnBy")),
            "size": size_lookup.get(f"{product_lookup.get(data.get('url_name'))}_{data.get('size')}"),
        }
        for data in cart_data
        if isinstance(data, dict) and "url_name" in data and data.get("url_name") in product_lookup
    ]

    return [Cart(
        **kwarg) for kwarg in kwargs_list if not any(value is None for key, value in kwarg.items() if key != "user")]


def update_user_cart(user: User, cart_data: list[dict[str, str]]) -> list[Cart] | list:
    if isinstance(cart_data, list):
        cart_list = clean_cart_list(cart_data, user)
        Cart.objects.bulk_create(
            cart_list, ignore_conflicts=True) if cart_list else []
        cart_data = get_cart_list(Cart.objects.filter(user=user))
        return cart_data

    else:
        return []
