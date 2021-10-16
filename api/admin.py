from django.contrib import admin
from .models import Product


# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    fields = ['slug', 'title', 'code', 'user', 'price', 'discount']


admin.site.register(Product, ProductAdmin)
