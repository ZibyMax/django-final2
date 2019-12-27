from django.contrib.auth.models import User
from django.db import models

ORDER_STATUS = (
    ('new', 'новый'),
    ('processing', 'обработка'),
    ('executed', 'выполнен'),
    ('error', 'ошибка')
)


class Store(models.Model):
    name = models.CharField(max_length=255)
    user = models.OneToOneField(User, on_delete=models.PROTECT)

    class Meta:
        verbose_name = 'Магазин'
        verbose_name_plural = "Список магазинов"
        ordering = ('name',)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = "Список категорий"
        ordering = ('name',)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, blank=True, null=True)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = "Список товаров"
        ordering = ('-name',)

    def __str__(self):
        return self.name


class PriceItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    cost = models.FloatField()

    class Meta:
        verbose_name = 'Позиция прайс-листа'
        verbose_name_plural = "Список позиций прайс-листов"

    def __str__(self):
        return f'{self.product} ({self.quantity} x {self.cost})'


class Price(models.Model):
    store = models.ForeignKey(Store, on_delete=models.PROTECT)
    date = models.DateTimeField(auto_now_add=True, auto_now=False)
    price_items = models.ManyToManyField(PriceItem)

    class Meta:
        verbose_name = 'Прайс-лист'
        verbose_name_plural = "Прайс-листы"
        ordering = ('-date',)

    def __str__(self):
        return f'{self.store.name} price'


class Parameter(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'Параметр товара'
        verbose_name_plural = "Список параметров товаров"

    def __str__(self):
        return self.name


class ProductParameter(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    parameter = models.ForeignKey(Parameter, on_delete=models.PROTECT)
    value = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'Характеристики товара'
        verbose_name_plural = "Список характеристик товаров"

    def __str__(self):
        return f'{self.product.name} ({self.parameter.name}={self.value})'


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    cost = models.FloatField()

    class Meta:
        verbose_name = 'Позиция заказа'
        verbose_name_plural = "Список позиций заказов"


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    store = models.ForeignKey(Store, on_delete=models.PROTECT)
    date = models.DateTimeField(auto_now_add=True, auto_now=False)
    order_items = models.ManyToManyField(OrderItem)
    status = models.CharField(max_length=255, choices=ORDER_STATUS, default='new')

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = "Список заказов"
        ordering = ('-date',)

    def __str__(self):
        return f'{self.store.name} - {self.user.username} order'

