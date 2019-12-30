# Дипломная работа к профессии Python-разработчик «API Сервис заказа товаров для розничных сетей».

## Описание API

### admin-getgoods/user/
**post: Регистрация нового пользователя для работы с приложением**

Обязательные поля:
- "email" - адрес электронной почты пользователя. Будет использован в качестве имени пользователя
- "password" - пароль для работы с приложением

Ограничений доступа нет.

Приложение использует для аутентификации пользователей Basic Authentication.
Имя пользователя (email) и пароль необходимо передавать с каждым запросом.
Регистрация позволяет получать прайс-листы с предложениями поставщиков и отправлять заказы.


### admin-getgoods/recover/
**post: Восстановление пароля пользователя**

Обязательное поле:
- "email" - если пользователь с таким адресом зарегистрирован, на почту будет выслан новый пароль

Ограничений доступа нет.


### admin-getgoods/reset/
**post: Изменение пароля пользователя**

Обязательное поле:
- "password" - новый пароль для работы с приложением

Для изменения пароля пользователь должен пройти аутентификацию.


### admin-getgoods/store/
**post: Регистрация пользователя как поставщика**

Обязательное поле:
- "name" - название магазина

Для регистрации магазина пользователь должен пройти аутентификацию.


### api/category, api/product, api/parameter, api/productparameter
**Управление категориями товаров, товарами и параметрами товаров**

Позволяет создавать/редактировать/удалять/получать информацию о категориях товаров, самих товарах и
характеристиках товаров.

Доступно только для поставщиков.


### price/ (price/<store_id>/)
**get: Получение прайс-листа**

Получение прайс-листа от зарегистрированных поставщиков (отдельного поставщика).

Доступно всем зарегистрированным пользователям.


### store-price/
**get: Получение поставщиком своего прайc-листа**

**post: Регистрация в приложении нового прайс-листа своего магазина**

Основное поле: "price" - список объектов, содержащих следующие поля:
"product" - id товара,
"quantity" - количество товаров,
"cost" - цена единицы товара

Доступно только для поставщиков.


### order/
**get: Получение списка своих заказов**

**post: Размещение заказа**

Отправляемые поля:
"store" - id магазина в который совершается заказ,
"order" - список объектов ("product", "quantity", "cost") с данными заказа
Количество заказываемых товаров должно быть меньше или равно количеству товаров в прайсе магазина.
Стоимость товаров должна совпадать со стоимостью в прайс-листе.

### store-order/
**get: Получение списка заказов своего магазина**

## Инструкция по установке

- Установите зависимости: pip install -r requirements.txt
- Формируем базу данных: manage.py makemigrations
- Выполните миграции: manage.py migrate
- Загрузите тестовые данные в базу: manage.py loaddata db.json
- Запустите тестовый сервер manage.py runserver

Данные тестовых пользователей (логин: пароль):

- store1@gg.com: store1
- store2@gg.com: store2
- store3@gg.com: store3
- juststore@gg.com: juststore

Схема Open API
https://documenter.getpostman.com/view/9210267/SWLbAVYL