from django.contrib import admin
from .models import Product, Slider, Banner
from .models import Category
from .models import ProductTag
from .models import Notification
from .models import Like
from .models import DeliveryModeItem
from .models import Comment
from .models import OrderItem
from .models import Shipping
from .models import ShippingStatus
from .models import DeliveryMode
from .models import Brand
from .models import Order
from .models import GalleryImage
from .models import Address
from .models import Country

# Register your models here.
# class ProductAdmin(admin.ModelAdmin):
#     fields = ['slug', 'title', 'code', 'user', 'price', 'discount', 'image']


admin.site.register(Address)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Notification)
admin.site.register(Slider)
admin.site.register(Banner)
admin.site.register(ProductTag)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Brand)
admin.site.register(Order)
admin.site.register(GalleryImage)
admin.site.register(DeliveryMode)
admin.site.register(DeliveryModeItem)
admin.site.register(OrderItem)
admin.site.register(ShippingStatus)
admin.site.register(Shipping)
admin.site.register(Country)
