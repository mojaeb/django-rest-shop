from django.conf import settings
from django.core.validators import RegexValidator
from django.db import models


class Brand(models.Model):
    name = models.CharField(max_length=50)
    slug = models.CharField(max_length=50)
    image = models.ImageField(upload_to='brands')

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.CharField(max_length=50)
    show_in_home = models.BooleanField(default=False)
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name


class DeliveryMode(models.Model):
    name = models.CharField(max_length=100)
    slug = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class DeliveryModeItem(models.Model):
    name = models.CharField(max_length=100)
    slug = models.CharField(max_length=100)
    delivery_mode = models.ForeignKey(
        DeliveryMode,
        on_delete=models.CASCADE,
        related_name='delivery_mode_items'
    )

    def __str__(self):
        return self.name


class ProductTag(models.Model):
    name = models.CharField(max_length=100)
    slug = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class GalleryImage(models.Model):
    image = models.ImageField(upload_to='images')

    def __str__(self):
        return str(self.image)


class Country(models.Model):
    name = models.CharField(max_length=20)
    slug = models.CharField(max_length=20)

    def __str__(self) -> str:
        return self.name


class Product(models.Model):
    title = models.CharField(max_length=200)
    slug = models.CharField(max_length=200, null=False)
    image = models.ImageField(upload_to='images', null=True)
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT, null=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(ProductTag)
    gallery = models.ManyToManyField(GalleryImage)
    details = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    country = models.ForeignKey(Country, null=True, blank=True, on_delete=models.PROTECT)
    variable_price = models.BooleanField(default=False)

    @property
    def min_price(self):
        if self.variants.count():
            return self.variants.first().price
        return 0

    @property
    def min_price_after_discount(self):
        if self.variants.count():
            return self.variants.first().price_after_discount
        return 0

    @property
    def max_discount(self):
        if self.variants.count():
            return self.variants.first().discount
        return 0

    @property
    def variants_length(self):
        return len(self.variants.all())

    @property
    def total_quantity(self):
        if self.variants.count():
            return sum([variant.quantity for variant in self.variants.all()])
        return 0

    def __str__(self):
        return self.title


class OptionType(models.Model):
    name = models.CharField(max_length=10)
    slug = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class OptionValue(models.Model):
    name = models.CharField(max_length=10)
    slug = models.CharField(max_length=10)
    type = models.ForeignKey(OptionType, on_delete=models.PROTECT)

    def __str__(self):
        return self.name


class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name="variants")
    code = models.IntegerField(default=0, blank=True)
    price = models.IntegerField(null=True)
    discount = models.IntegerField(blank=True, default=0)
    discount_due_date = models.DateTimeField(null=True, blank=True)
    weight = models.IntegerField()
    quantity = models.IntegerField(default=0)
    variable_price = models.BooleanField(default=False)

    @property
    def price_after_discount(self):
        return self.price - self.discount

    class Meta:
        ordering = ['price', '-discount']

    def __str__(self):
        return "{} {}".format(str(self.product), self.price)


class VariantOption(models.Model):
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, related_name="options")
    type = models.ForeignKey(OptionType, on_delete=models.PROTECT)
    value = models.ForeignKey(OptionValue, on_delete=models.PROTECT)

    def __str__(self):
        return "{} {}".format(str(self.type), str(self.value))


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} >> {}".format(self.product.title, self.text)


class Like(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class Address(models.Model):
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    city_code = models.CharField(max_length=10)
    state_code = models.CharField(max_length=10)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=200)
    is_mine = models.BooleanField(default=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '+999999999'. Up to 15 digits "
                                         "allowed.")
    house_number = models.IntegerField(null=True, blank=True)
    unit = models.IntegerField(null=True, blank=True)
    zip_code = models.IntegerField()
    phone_number = models.CharField(
        validators=[phone_regex], max_length=17, blank=True)  # validators should be a list
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)


# shopping models
class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    payment_succeed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    amount = models.IntegerField(default=None, null=True, blank=True)
    discount_amount = models.IntegerField(default=None, blank=True, null=True)
    deleted_at = models.DateTimeField(null=True, blank=True, default=None)
    address = models.ForeignKey(
        Address, null=True, on_delete=models.SET_NULL, blank=True, related_name='orders')
    authority = models.CharField(max_length=200, null=True, blank=True)
    pay_url = models.URLField(null=True, blank=True)
    canceled = models.BooleanField(default=False)
    ref_id = models.CharField(null=True, blank=True, max_length=200)
    checkout_datetime = models.DateTimeField(blank=True, null=True)
    success_payment_datetime = models.DateTimeField(blank=True, null=True)
    warehouse_confirmation = models.BooleanField(default=False)
    delivered = models.BooleanField(default=False)
    returned = models.BooleanField(default=False)

    @property
    def total_price(self):
        return sum(item.total_price for item in self.order_items.all())

    @property
    def total_discount(self):
        return sum(item.total_discount for item in self.order_items.all())

    @property
    def total_price_after_discount(self):
        return sum(item.total_price_after_discount for item in self.order_items.all())

    @property
    def total_weight(self):
        return sum([o.product_variant.weight for o in self.order_items.all()])


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    product_variant = models.ForeignKey(ProductVariant, on_delete=models.PROTECT)
    quantity = models.IntegerField(default=0)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def total_price(self):
        return self.product_variant.price * self.quantity

    @property
    def total_discount(self):
        return self.product_variant.discount * self.quantity

    @property
    def total_price_after_discount(self):
        return self.total_price - self.total_discount


class ShippingStatus(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=10)


class Shipping(models.Model):
    status = models.ForeignKey(ShippingStatus, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)


class Notification(models.Model):
    title = models.CharField(max_length=200)
    url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Slider(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    url = models.CharField(max_length=200)
    image = models.ImageField(upload_to='sliders')


class Banner(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    url = models.CharField(max_length=200)
