# Социальная сеть YaTube.

Социальная сеть с возможностью создания, просмотра, редактирования и удаления (CRUD) записей. Возможность добавления изображений.
Реализован механизм подписки на понравившихся авторов и отслеживание их записей.
Покрытие тестами.
Подключены пагинация, кеширование, авторизация пользователя, возможна смена пароля через почту.


Инструментарий:

Django 2.2
Python 3.9
Django Unittest
Django debug toolbar
PostgreSQL
Django ORM

Запуск:
  Установка зависимостей:
    <pip install -r requirements.txt>

  Применение миграций:
    <python manage.py makemigrations>
    <python manage.py migrate>

  Создание администратора:
    <python manage.py createsuperuser>

  Запуск приложения:
    <python manage.py runserver>
      

Проект размещен по адресу: catrain2020-ya.tk
