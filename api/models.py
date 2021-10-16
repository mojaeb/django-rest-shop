from django.db import models


# Create your models here.


class Product(models.Model):
    slug = models.CharField(max_length=200, null=False)
    title = models.CharField(max_length=200)
    code = models.CharField(max_length=50)

    def __str__(self):
        return self.title
