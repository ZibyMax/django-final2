from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Store, Category, Product, PriceItem, Price, Parameter, ProductParameter, OrderItem, Order


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        extra_kwargs = {
            'username': {'write_only': True},
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        return User.objects.create_user(validated_data['username'],
                                        validated_data['email'],
                                        validated_data['password'])


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ('id', 'name', 'user')
        extra_kwargs = {
            'user': {'write_only': True},
        }


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')


class ParameterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parameter
        fields = ('id', 'name')


class ProductParameterPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductParameter
        fields = ('parameter', 'value')

    parameter = serializers.StringRelatedField()


class ProductParameterSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductParameter
        fields = ('product', 'parameter', 'value')


class ProductPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name', 'category', 'parameters')

    category = CategorySerializer()
    parameters = serializers.SerializerMethodField()

    def get_parameters(self, obj):
        parameters = ProductParameter.objects.filter(product=obj)
        serializer = ProductParameterPriceSerializer(parameters, many=True)
        return serializer.data


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name', 'category')


class PriceItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceItem
        fields = ('product', 'quantity', 'cost')

    product = ProductPriceSerializer()


class ImportPriceItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceItem
        fields = ('product', 'quantity', 'cost')


class StorePriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ('id', 'name', 'price')

    price = serializers.SerializerMethodField()

    def get_price(self, obj):
        price = Price.objects.filter(store=obj).order_by('date').last()
        if price is None:
            return None
        serializer = PriceItemSerializer(price.price_items.all(), many=True)
        return serializer.data


class PriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Price
        fields = ('store', 'date', 'price_items')

    price_items = PriceItemSerializer(many=True)


class ImportOrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ('product', 'quantity', 'cost')


class ExportOrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ('product', 'quantity', 'cost')

    product = serializers.StringRelatedField()


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('store', 'date', 'status', 'order_items')

    store = serializers.StringRelatedField()
    order_items = ExportOrderItemSerializer(many=True)
