from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated, BasePermission
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from .serializers import CategorySerializer, ParameterSerializer, ProductSerializer, ProductParameterSerializer, \
    UserSerializer, StoreSerializer, PriceSerializer
from .models import Category, Parameter, Product, ProductParameter, Store, Price


# Обработка категорий товаров
class APICategoryViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


# Обработка параметров
class APIParameterViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Parameter.objects.all()
    serializer_class = ParameterSerializer


# Обработка товаров
class APIProductViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated, )
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


# Обработка параметров товаров
class APIProductParameterViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated, )
    queryset = ProductParameter.objects.all()
    serializer_class = ProductParameterSerializer


# Создание нового пользователя
# Имя пользователя = адрес электронной почты
class RegisterUserView(APIView):
    permission_classes = (AllowAny, )

    def post(self, request):
        data = request.data
        if 'username' in data:
            data['email'] = data['username']
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
            return Response({'error': 'user already has store'}, status=status.HTTP_400_BAD_REQUEST)
        data['user'] = request.user.id
        serializer = StoreSerializer(data=data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


# Доступ только для пользователей зарегистрировавших магазин
class IsShopOwner(BasePermission):
    def has_permission(self, request):
        user_has_store = Store.objects.filter(user=request.user).exists()
        return bool(request.user and request.user.is_authenticated and user_has_store)


class PriceView(APIView):
    permission_classes = (AllowAny, )

    def get(self, request, store_id=None):
        if store_id is None:
            queryset = Store.objects.all()
        elif Store.objects.filter(pk=store_id).exists():
            queryset = Store.objects.get(pk=store_id)
        else:
            return Response({'error': 'Store not found.'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = PriceSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
