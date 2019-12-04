from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Store, Category, Product, PriceItem, Price, Parameter, ProductParameter


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


class ProductParameterSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductParameter
        fields = ('parameter', 'value')

    parameter = serializers.StringRelatedField()


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name', 'category', 'parameters')

    category = CategorySerializer()
    parameters = serializers.SerializerMethodField()

    def get_parameters(self, obj):
        parameters = ProductParameter.objects.filter(product=obj)
        serializer = ProductParameterSerializer(parameters, many=True)
        return serializer.data


class PriceItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceItem
        fields = ('product', 'quantity', 'cost')

    product = ProductSerializer()


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
        price = Price.objects.filter(store=obj).order_by('data').last()
        serializer = PriceItemSerializer(price.price_items.all(), many=True)
        return serializer.data


class PriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Price
        fields = ('store', 'data', 'price_items')

    price_items = serializers.SerializerMethodField()

    def get_price_items(self, obj):
        serializer = PriceItemSerializer(obj.price_items.all(), many=True)
        return serializer.data