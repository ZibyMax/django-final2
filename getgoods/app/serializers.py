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
        fields = ('id', 'product', 'parameter', 'value')


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name', 'category')


class PriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ('id', 'name', 'price')

    price = serializers.SerializerMethodField()

    def get_price(self, obj):
        return 'Йооохууу!'
