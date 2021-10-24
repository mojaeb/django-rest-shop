import requests
from django.conf import settings

from . import urls


def calculate_order_prices(order_items):
    total_price = 0
    total_discount = 0
    for order_item in order_items:
        total_price += order_item.product.price
        total_discount += order_item.product.discount

    total_price_after_discount = (total_price - total_discount)

    return {
        'total_price': total_price,
        'total_discount': total_discount,
        'total_price_after_discount': total_price_after_discount
    }


def is_true(literal):
    # literal to boolean
    return bool('true' in str(literal).lower())


def calculate_shipping_price(price, weight, state, city):
    params = {
        "rate_type": "tapin",
        "price": price,
        "weight": weight,
        "order_type": "0",
        "pay_type": "1",
        "from_province": settings.SOURCE_STATE_CODE,
        "from_city": settings.SOURCE_CITY_CODE,
        "to_province": str(state),
        "to_city": str(city),
    }
    try:
        result = requests.post(urls.CHECK_SHIPPING_PRICE, data=params)
    except requests.RequestException as err:
        return None, err
    data = result.json()
    total = int(data['entries']['total'])
    return total, None
