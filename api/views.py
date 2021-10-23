from django.core.paginator import Paginator
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_201_CREATED, HTTP_404_NOT_FOUND
from rest_framework.status import HTTP_204_NO_CONTENT
from .models import Comment, Category, Brand
from .models import Like, Address, Banner, Slider, Order, OrderItem
from .models import Notification
from .models import Product
from .serializers import ProductByIdSerializer, LikeSerializer, BrandSerializer, CategorySerializer
from .serializers import ProductSerializer, NotificationsSerializer, AddressesSerializer, BannerSerializer
from .serializers import SliderSerializer, OrderSerializer
import requests
from . import urls

# TODO search with parameters
# TODO pagination
# filter with pass category_id, product_title, tag_id, banner_id, between price number,
# has in warehouse
from .utils import is_true, calculate_shipping_price


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_query_param = 'page'
    page_size_query_param = 'per_page'
    max_page_size = 1000


@api_view(['POST'])
def get_products(request):
    filters = {}
    for key, value in request.data.items():
        filters[key] = value
    products = Product.objects.filter(**filters)
    len_product = len(products)
    if len_product > 0:
        paginator = StandardResultsSetPagination()
        result_page = paginator.paginate_queryset(products, request)
        serializer = ProductSerializer(result_page, many=True)
        return Response(
            {
                'data': serializer.data,
                'pagination': {
                    'page': int(paginator.get_page_number(request, paginator)),
                    'per_page': paginator.get_page_size(request),
                    'count': len_product
                }
            },
            status=HTTP_200_OK,
        )
    else:
        return Response({'data': []})


@api_view(['GET'])
def get_brands(request):
    products = Brand.objects.all()
    serializer = BrandSerializer(products, many=True)
    return Response(
        {'data': serializer.data},
        status=HTTP_200_OK
    )


@api_view(['GET'])
def get_categories(request):
    products = Category.objects.all()
    serializer = CategorySerializer(products, many=True)
    return Response(
        {'data': serializer.data},
        status=HTTP_200_OK
    )


@api_view(['GET'])
def get_product(request, pid):
    try:
        product = Product.objects.get(pk=pid)
    except Product.DoesNotExist:
        return Response(
            {'error': 'bad request'},
            status=HTTP_400_BAD_REQUEST
        )
    serializer = ProductByIdSerializer(product)
    return Response(
        {'data': serializer.data},
        status=HTTP_200_OK
    )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def like_product(request, pid):
    user = request.user
    Like.objects.get_or_create(user=user, product_id=pid)
    return Response(
        {'data': 'liked was successful'},
        status=HTTP_201_CREATED
    )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def unlike_product(request, pid):
    user = request.user
    Like.objects.get(user=user, product_id=pid).delete()
    return Response(
        {'data': 'unlike was successful'},
        status=HTTP_200_OK
    )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_likes(request):
    user = request.user
    try:
        likes = Like.objects.filter(user=user)
    except Like.DoesNotExist:
        return Response(
            {'error': 'not found'},
            status=HTTP_404_NOT_FOUND
        )
    serializer = LikeSerializer(likes, many=True)
    return Response({'data': serializer.data}, status=HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_comment(request, pid):
    user = request.user
    if not ('text' in request.data):
        return Response(
            {'error': 'bad request'},
            status=HTTP_400_BAD_REQUEST
        )
    Comment.objects.create(
        user=user,
        product_id=pid,
        text=request.data['text']
    )
    return Response(
        {'data': 'comment added'},
        status=HTTP_201_CREATED
    )


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_comment(request, cid):
    Comment.objects.get(id=cid).delete()
    return Response(
        {'data': 'deleted was successful'},
        status=HTTP_200_OK
    )


# crud address
# start
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_addresses(request):
    user = request.user
    addresses = Address.objects.filter(user=user)
    serializer = AddressesSerializer(addresses, many=True)
    return Response(
        {'data': serializer.data},
        status=HTTP_200_OK
    )


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def address(request, aid):
    user = request.user
    try:
        address = Address.objects.get(id=aid, user=user)
    except Address.DoesNotExist:
        return Response({'error': 'no found'}, status=HTTP_404_NOT_FOUND)
    if request.method == 'PUT':
        serializer = AddressesSerializer(address, data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({'data': serializer.data}, status=HTTP_200_OK)
        return Response({'error': serializer.errors}, status=HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        address.delete()
        return Response({'data': 'deleted was successful'}, status=HTTP_204_NO_CONTENT)
    serializer = AddressesSerializer(address)
    return Response(
        {'data': serializer.data},
        status=HTTP_200_OK
    )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_address(request):
    serializer = AddressesSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response({'data': serializer.data}, status=HTTP_200_OK)
    return Response({'error': serializer.errors}, status=HTTP_400_BAD_REQUEST)


# end crud address


@api_view(['GET'])
def get_sliders(request):
    sliders = Slider.objects.all()
    serializer = SliderSerializer(sliders, many=True)
    return Response(
        {'data': serializer.data},
        status=HTTP_200_OK
    )


@api_view(['GET'])
def get_banners(request):
    banners = Banner.objects.all()
    serializer = BannerSerializer(banners, many=True)
    return Response(
        {'data': serializer.data},
        status=HTTP_200_OK
    )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_cart(request, product_id, quantity):
    user = request.user
    order = Order.objects.get_or_create(payment_succeed=False, user=user)
    order = order[0]
    product = Product.objects.get(pk=product_id)
    order_item, created = OrderItem.objects.get_or_create(
        order=order,
        user=user,
        product_id=product_id
    )
    if product.quantity >= (order_item.quantity + quantity):
        if created:
            order_item.quantity = quantity
            order_item.save()
        else:
            order_item.quantity = order_item.quantity + quantity
            order_item.save()
        return Response(
            {'data': 'product added to cart'},
            status=HTTP_200_OK
        )
    else:
        return Response(
            {'error': "product hasn't {} quantity".format(quantity)},
            status=HTTP_204_NO_CONTENT
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def remove_from_cart(request, order_item_id):
    order = OrderItem.objects.get(pk=order_item_id)
    order.delete()
    return Response({'data': 'deleted was successful'}, status=HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def cart(request):
    user = request.user
    try:
        order, created = Order.objects.get_or_create(payment_succeed=False, user=user)
    except Order.DoesNotExist:
        return Response(
            {'error': 'not found'},
            status=HTTP_404_NOT_FOUND
        )
    if order.address is None:
        last_address = Address.objects.filter(user=user)
        if len(last_address):
            order.address = last_address[0]
            order.save()
    serializer = OrderSerializer(order)
    has_shipping_price = is_true(request.query_params.get('has_shipping_price'))
    if has_shipping_price and order.order_items.count():
        shipping_price = calculate_shipping_price(
            order.total_price_after_discount,
            order.total_weight,
            city=order.address.city_code,
            state=order.address.state_code,
        )
        return Response({
            'data': {
                **serializer.data,
                'shipping_price': shipping_price,
                'total_price_after_shipping': order.total_price_after_discount + shipping_price
            }
        })
    return Response({
        'data': serializer.data
    })


def change_order_address(request, address_id):
    user = request.user
    order = Order.objects.get(payment_succeed=False, user=user)
    order.address_id = address_id
    order.save()
    return Response({
        'data': 'change address was successful'},
        status=HTTP_200_OK
    )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def checkout(request):
    user = request.user
    order = Order.objects.get(payment_succeed=False, user=user)
    # validation request and check entity requirements
    if order.order_items.count() < 1:
        return Response(
            {'error': 'empty cart item'},
            status=HTTP_204_NO_CONTENT
        )
    if order.address is None:
        return Response(
            {'error': 'address not found'},
            status=HTTP_404_NOT_FOUND
        )
    shipping_price, error = calculate_shipping_price(
        order.total_price_after_discount,
        order.total_weight,
        city=order.address.city_code,
        state=order.address.state_code,
    )
    if not error:
        # payment functionality
        # payment with zarinpal
        data = {
            'merchant_id':
        }
        return Response(shipping_price)
    return Response(
        {'error': 'checkout has some error'},
        status=HTTP_400_BAD_REQUEST
    )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def increase_quantity(request, order_item_id):
    user = request.user
    order_item = OrderItem.objects.get(pk=order_item_id, user=user)
    product_quantity = order_item.product.quantity
    if product_quantity >= (order_item.quantity + 1):
        return Response(
            {'data': 'increment was successful'},
            status=HTTP_200_OK
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def decrease_quantity(request, order_item_id):
    user = request.user
    order_item = OrderItem.objects.get(pk=order_item_id, user=user)
    product_quantity = order_item.product.quantity
    current_quantity = order_item.quantity - 1
    if product_quantity >= current_quantity > 0:
        return Response(
            {'data': 'decrement was successful'},
            status=HTTP_200_OK
        )
    elif current_quantity == 0:
        order_item.delete()
        return Response(
            {'data': 'order deleted was successful'},
            status=HTTP_204_NO_CONTENT
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_notifications(request):
    notifications = Notification.objects.all()
    serializer = NotificationsSerializer(notifications, many=True)
    return Response(
        {'data': serializer.data},
        status=HTTP_200_OK
    )


'''
TODO followed bottom view sets was not important in this version
when complete add this functions into the project 

def change_order_pay_method(request):
def change_order_delivery_mode():
def bulk_add_to_cart():
def orders(request):

'''
