from django.conf import Settings
from rest_framework import serializers
from .models import Comment, Country, GalleryImage, Product, Banner, Slider, Order, OrderItem, Like, ProductVariant, \
    OptionType, VariantOption
from .models import Address
from .models import ProductTag
from .models import DeliveryMode
from .models import DeliveryModeItem
from .models import Category
from .models import Brand
from .models import Notification

import requests
from django.conf import settings
from . import urls
from django.contrib.auth import get_user_model


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = [
            'id',
            'email',
            'is_superuser',
            'user_name',
            'profile_image',
            'first_name',
            'last_name',
            'email',
            'phone_number',
        ]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = [
            'id',
            'is_superuser',
            'user_name',
            'profile_image',
            'first_name',
            'last_name',
            'phone_number',
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
            'slug',
            'parent_id'
        ]


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = Product
        fields = [
            'id',
            'slug',
            'title',
            'image',
            'category',
            'min_price',
            'max_discount',
            'variants_length',
            'total_quantity',
            'min_price_after_discount',
            'variable_price',
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


class GallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = GalleryImage
        fields = [
            'image',
        ]


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = [
            'id',
            'name',
            'slug',
        ]


class OptionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = OptionType
        fields = [
            'id',
            'name',
            'slug',
        ]


class OptionValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = OptionType
        fields = [
            'id',
            'name',
            'slug',
        ]


class VariantOptionSerializer(serializers.ModelSerializer):
    type = OptionTypeSerializer()
    value = OptionValueSerializer()

    class Meta:
        model = VariantOption
        fields = [
            'id',
            'type',
            'value',
        ]


class ProductVariantSerializer(serializers.ModelSerializer):
    options = VariantOptionSerializer(many=True)

    class Meta:
        model = ProductVariant
        fields = [
            'id',
            'options',
            'price',
            'discount',
            'code',
            'discount_due_date',
            'weight',
            'quantity',
            'price_after_discount',
            'variable_price',
        ]


class ProductByIdSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    category = CategorySerializer()
    brand = BrandSerializer()
    gallery = GallerySerializer(many=True)
    country = CountrySerializer()
    variants = ProductVariantSerializer(many=True)

    class Meta:
        model = Product
        fields = [
            'id',
            'slug',
            'title',
            'image',
            'brand',
            'category',
            'created_at',
            'gallery',
            'tags',
            'country',
            'details',
            'description',
            'variants',
            'variable_price',
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
    user = UserSerializer(required=False)
    house_number = serializers.IntegerField(required=False)
    unit = serializers.IntegerField(required=False)

    class Meta:
        model = Address
        fields = [
            'id',
            'city',
            'user',
            'city_code',
            'state_code',
            'state',
            'location',
            'address',
            'is_mine',
            'phone_number',
            'first_name',
            'last_name',
            'house_number',
            'unit',
            'zip_code',
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


class AbstractProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'id',
            'slug',
            'title',
            'image',
            'category',
        ]


class AbstractVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        fields = [
            'id',
            'price',
            'discount',
            'code',
            'discount_due_date',
            'weight',
            'quantity',
        ]


class OrderItemSerializer(serializers.ModelSerializer):
    product = AbstractProductSerializer()
    product_variant = AbstractVariantSerializer()

    class Meta:
        model = OrderItem
        fields = [
            'id',
            'product',
            'quantity',
            'order',
            'product_variant',
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
            'warehouse_confirmation',
            'delivered',
            'returned',
        ]


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Comment
        fields = [
            'user',
            'text',
            'created_at',
            'product'
        ]


class LikeSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = Like
        fields = [
            'product'
        ]
