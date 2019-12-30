from django.contrib import admin

from .models import Category, Product, PriceItem, Store, Parameter, ProductParameter, Price, Order, OrderItem


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    pass


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass


@admin.register(PriceItem)
class PriceItemAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity', 'cost',)


@admin.register(Price)
class PriceAdmin(admin.ModelAdmin):
    list_display = ('store', 'date')


@admin.register(Parameter)
class ParameterAdmin(admin.ModelAdmin):
    pass


@admin.register(ProductParameter)
class ProductParameterAdmin(admin.ModelAdmin):
    pass


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'store', 'date',)


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity', 'cost',)

