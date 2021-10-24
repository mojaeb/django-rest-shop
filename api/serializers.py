from rest_framework import serializers
from .models import Product, Banner, Slider, Order, OrderItem, Like
from .models import Address
from .models import ProductTag
from .models import DeliveryMode
from .models import DeliveryModeItem
from .models import Category
from .models import Brand
from .models import Notification
import requests

from . import urls


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'id',
            'slug',
            'title',
            'code',
            'image',
            'price',
            'discount',
            'quantity',
        ]


class DeliveryModeItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryModeItem
        fields = ['name', 'slug']


class DeliveryModeSerializer(serializers.ModelSerializer):
    delivery_mode_items = DeliveryModeItemSerializer(many=True, read_only=True)

    class Meta:
        model = DeliveryMode
        fields = ['name', 'slug', 'delivery_mode_items']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductTag
        fields = ['name', 'slug', 'id']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            'id',
            'name',
            'slug'
        ]


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = [
            'id',
            'name',
            'slug',
            'image',
        ]


class ProductByIdSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    delivery_mode = DeliveryModeSerializer()
    category = CategorySerializer()
    brand = BrandSerializer()

    class Meta:
        model = Product
        fields = [
            'id',
            'slug',
            'title',
            'code',
            'image',
            'price',
            'discount',
            'brand',
            'category',
            'created_at',
            'gallery',
            'quantity',
            'tags',
            'delivery_mode',
            'weight',
        ]


class NotificationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = [
            'title',
            'url',
            'created_at',
        ]


class AddressesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = [
            'id',
            'city',
            'city_code',
            'state_code',
            'state',
            'location',
            'address',
            'is_mine',
            'phone_number',
            'person_name',
        ]


class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = [
            'id',
            'title',
            'description',
            'url'
        ]


class SliderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slider
        fields = [
            'id',
            'title',
            'description',
            'url',
            'image',
        ]


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = OrderItem
        fields = [
            'id',
            'product',
            'quantity',
            'order',
            'created_at',
            'total_price',
            'total_discount',
            'total_price_after_discount',
        ]


class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True, read_only=True)
    address = AddressesSerializer()

    class Meta:
        model = Order
        fields = [
            'id',
            'payment_succeed',
            'created_at',
            'amount',
            'discount_amount',
            'deleted_at',
            'address',
            'order_items',
            'total_price',
            'total_discount',
            'total_price_after_discount',
            'total_weight',
            'pay_url',
            'authority',
            'canceled',
        ]


class LikeSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = Like
        fields = [
            'product'
        ]
