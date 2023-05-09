from django.db import models
from users.models import *

# Create your models here.
class ProductCategory(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, blank=True)
    quantity = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='products_images', blank=True)

    category = models.ForeignKey(to=ProductCategory,on_delete=models.CASCADE)

    def __str__(self):
        return self.name



class BasketQuerySet(models.QuerySet):
    def total_sum(self):
        # baskets = Basket.objects.filter(user=self.user)
        #
        # return sum(basket.sum() for basket in baskets)
        return sum(basket.sum() for basket in self)

    def total_quantity(self):
        return sum(basket.quantity for basket in self)


class Basket(models.Model):
    user = models.ForeignKey(to=User,on_delete=models.CASCADE)
    product = models.ForeignKey(to=Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    created_timestamp = models.DateTimeField(auto_now_add=True)

    objects = BasketQuerySet.as_manager()
    def __str__(self):
        return f'Корзина для {self.user.username} | Продукт: {self.product.name}'

    def sum(self):
        return self.product.price * self.quantity

