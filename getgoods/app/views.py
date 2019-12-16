from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated, BasePermission
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from .serializers import *
from .models import Category, Parameter, Product, ProductParameter, Store, Price, Order


# Доступ только для пользователей зарегистрировавших магазин
class IsShopOwner(BasePermission):
    def has_permission(self, request, view):
        user_has_store = Store.objects.filter(user=request.user).exists()
        return bool(request.user and request.user.is_authenticated and user_has_store)


# Обработка категорий товаров
class APICategoryViewSet(ModelViewSet):
    permission_classes = (IsShopOwner,)
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


# Обработка параметров
class APIParameterViewSet(ModelViewSet):
    permission_classes = (IsShopOwner,)
    queryset = Parameter.objects.all()
    serializer_class = ParameterSerializer


# Обработка товаров
class APIProductViewSet(ModelViewSet):
    permission_classes = (IsShopOwner,)
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


# Обработка параметров товаров
class APIProductParameterViewSet(ModelViewSet):
    permission_classes = (IsShopOwner,)
    queryset = ProductParameter.objects.all()
    serializer_class = ProductParameterSerializer


# Создание нового пользователя
# Имя пользователя = адрес электронной почты
class RegisterUserView(APIView):
    permission_classes = (AllowAny, )

    def post(self, request):
        data = request.data
        if 'email' in data:
            data['username'] = data['email']
        serializer = UserSerializer(data=data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)


# Восстановление пароля пользователя
# Если пользователь зарегистрирован, отптравляем ему на почту новый пороль
class RecoverUserView(APIView):
    permission_classes = (AllowAny, )

    def post(self, request):
        if 'email' not in request.data:
            return Response({'error': 'field "email" is required'}, status=status.HTTP_400_BAD_REQUEST)
        queryset = User.objects.filter(username=request.data['email'])
        if not queryset.exists():
            return Response({'error': 'user not found'}, status=status.HTTP_400_BAD_REQUEST)
        user = queryset.first()
        password = User.objects.make_random_password()
        user.set_password(password)
        user.save()

        # ПРОБЛЕМКА)))
        # user.email_user(
        #     'Password recovery',
        #     f'New password: {new_password}',
        # )

        return Response({'password': password}, status=status.HTTP_200_OK)


# Изменение пароля пользователя
# Пользователь должен быть зарегистрирован и авторизован
class ResetUserView(APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request):
        if 'password' not in request.data:
            return Response({'error': 'Field "password" is required.'}, status=status.HTTP_400_BAD_REQUEST)
        request.user.set_password(request.data['password'])
        request.user.save()
        return Response(status=status.HTTP_200_OK)


# Регистрация нового магазина на авторизованного пользователя
class RegisterStoreView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        data = request.data
        if 'name' not in data:
            return Response({'error': 'Field "name" is required.'}, status=status.HTTP_400_BAD_REQUEST)
        is_user_has_store = Store.objects.filter(user=request.user).exists()
        if is_user_has_store:
            return Response({'error': 'User already has store'}, status=status.HTTP_400_BAD_REQUEST)
        data['user'] = request.user.id
        serializer = StoreSerializer(data=data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


# Экспорт прайс-листа
class PriceView(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request, store_id=None):
        if store_id is None:
            queryset = Store.objects.all()
            serializer = StorePriceSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        if Store.objects.filter(pk=store_id).exists():
            queryset = Store.objects.get(pk=store_id)
            serializer = StorePriceSerializer(queryset)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Store not found.'}, status=status.HTTP_400_BAD_REQUEST)


# Экспорт и импорт прайс-листа магазина пользователя
class StorePriceView(APIView):
    permission_classes = (IsShopOwner, )

    def get(self, request):
        store = Store.objects.get(user=request.user)
        price = Price.objects.filter(store=store).order_by('date').last()
        serializer = PriceSerializer(price)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        store = Store.objects.get(user=request.user)
        if 'price' not in request.data:
            return Response({'error': 'Field "price" is required.'}, status=status.HTTP_400_BAD_REQUEST)
        price = Price(store=store)
        if not isinstance(request.data['price'], list):
            return Response('error: price should be a list', status=status.HTTP_400_BAD_REQUEST)
        price.save()
        for item in request.data['price']:
            serializer = ImportPriceItemSerializer(data=item)
            if serializer.is_valid():
                price_item = serializer.save()
                price.price_items.add(price_item)
            else:
                for saved_price_item in price.price_items.all():
                    saved_price_item.delete()
                price.delete()
                Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        price.save()
        return Response(status=status.HTTP_200_OK)


# Размещение заказов пользователя. Получение списка с историей заказов
class OrderView(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        queryset = Order.objects.select_related('store').prefetch_related('order_items').\
            filter(user=request.user).order_by('-date')
        serializer = OrderSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        if 'store' not in request.data:
            return Response({'error': 'Field "Store" is required.'}, status=status.HTTP_400_BAD_REQUEST)
        if 'order' not in request.data:
            return Response({'error': 'Field "Order" is required.'}, status=status.HTTP_400_BAD_REQUEST)
        stores = Store.objects.filter(pk=request.data['store'])
        if not stores.exists():
            return Response({'error': 'Store not found.'}, status=status.HTTP_400_BAD_REQUEST)
        store = stores.first()
        order = Order(store=store, user=request.user)
        if not isinstance(request.data['order'], list):
            return Response('error: order should be a list', status=status.HTTP_400_BAD_REQUEST)
        order.save()
        for item in request.data['order']:
            serializer = ImportOrderItemSerializer(data=item)
            if serializer.is_valid():
                order_item = serializer.save()
                order.order_items.add(order_item)
            else:
                for saved_order_item in order.order_items.all():
                    saved_order_item.delete()
                order.delete()
                Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        order.save()
        return Response(status=status.HTTP_200_OK)


# Получение магазином списка своих заказов
class StoreOrderView(APIView):
    permission_classes = (IsShopOwner, )

    def get(self, request):
        store = Store.objects.filter(user=request.user).first()
        queryset = Order.objects.filter(store=store).order_by('date')
        serializer = OrderSerializer(queryset, many=True)
        return Response(serializer.data)
