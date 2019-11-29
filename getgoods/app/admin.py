from django.contrib import admin

from .models import Category, Product, PriceItem, Store, Parameter, ProductParameter, Price


class StoreAdmin(admin.ModelAdmin):
    pass


class CategoryAdmin(admin.ModelAdmin):
    pass


class ProductAdmin(admin.ModelAdmin):
    pass


class PriceItemAdmin(admin.ModelAdmin):
    pass


class PriceAdmin(admin.ModelAdmin):
    pass


class ParameterAdmin(admin.ModelAdmin):
    pass


class ProductParameterAdmin(admin.ModelAdmin):
    pass


admin.site.register(Store, StoreAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(PriceItem, PriceItemAdmin)
admin.site.register(Price, PriceAdmin)
admin.site.register(Parameter, ParameterAdmin)
admin.site.register(ProductParameter, ProductParameterAdmin)
