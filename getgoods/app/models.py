from django.contrib.auth.models import User
from django.db import models

ORDER_STATUS = (
    ('new', 'новый'),
    ('processing', 'обработка'),
    ('executed', 'выполнен'),
)

class Store(models.Model):
    name = models.CharField(max_length=255)
    user = models.OneToOneField(User, on_delete=models.PROTECT)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, blank=True, null=True)

    def __str__(self):
        return self.name


class PriceItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    cost = models.FloatField()


class Price(models.Model):
    store = models.ForeignKey(Store, on_delete=models.PROTECT)
    date = models.DateTimeField(auto_now_add=True, auto_now=False)
    price_items = models.ManyToManyField(PriceItem)

    def __str__(self):
        return f'{self.store.name} price'


class Parameter(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class ProductParameter(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    parameter = models.ForeignKey(Parameter, on_delete=models.PROTECT)
    value = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.product.name} ({self.parameter.name}={self.value})'


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    cost = models.FloatField()


class Order(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT, blank=True, null=True)
    store = models.ForeignKey(Store, on_delete=models.PROTECT)
    date = models.DateTimeField(auto_now_add=True, auto_now=False)
    order_items = models.ManyToManyField(OrderItem)
    status = models.CharField(max_length=255, choices=ORDER_STATUS, default='new')

    def __str__(self):
        return f'{self.store.name} order'

