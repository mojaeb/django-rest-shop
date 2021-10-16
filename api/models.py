from django.db import models
# from .. import user


class Product(models.Model):
    slug = models.CharField(max_length=200, null=False)
    title = models.CharField(max_length=200)
    code = models.CharField(max_length=50)
    # user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL)
    price = models.IntegerField(null=True)
    discount = models.IntegerField(null=True)


    def __str__(self):
        return self.title
