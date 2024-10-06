# Workmate_cats
## 1. [Задание и требования](#1)
## 2. [Функционал API, эндпойнты и технические особенности](#2)
## 3. [Стек технологий](#3)
## 4. [Запуск проекта через docker compose и ссыылка на него](#4)
## 5. [Автор проекта:](#5)

## 1. Описание  <a id=1></a>
### Цель задания: Спроектировать REST API онлайн выставка котят.
API должно иметь следующие методы:
- Получение списка пород
- Получение списка всех котят
- Получение списка котят определенной породы по фильтру.
- Получение подробной информации о котенке.
- Добавление информации о котенке
- Изменение информации о котенке
- Удаление информации о котенке
- JWT Авторизация пользователей \
Бизнес логика: \
Каждый котенок должен иметь – цвет, возраст (полных месяцев) и описание. \
Удалять изменять или обновлять информацию пользователь может только о тех животных, которых он добавил сам. \
При возникновении неоднозначности в задаче – принятие конечного решения остается за кандидатом.\

## 2. Функционал API, эндпойнты и технические особенности <a id=2></a>

__Создан UserManager и кастомный пользователь CustUser с регистрацией по email. ()
Написана COLLECT_SCHEMA для документирования эндпойнтов.__
- http://localhost:8000/api/swagger/ реализована возможность автоматической генерации документации для API, с помощью Swagger
- https://localhost:8000/api/redoc/ реализована возможность автоматической генерации документации для API, с помощью Redoc
- http://localhost:8000/api/users/  Djoser эндпойнты. Работа с пользователями. Регистрация пользователей, удаление, 
изменение данных.Вывод пользователей. POST, GET, PUT, PATCH, DEL запросы.(Смотри документацию Swagger или Redoc).\
__Реализована JWT Авторизация пользователей. Подключен для безопасности rest_framework_simplejwt.token_blacklist__
- http://localhost:8000/api/auth/jwt/create/ Создание JWT-токена (Доступно: Кто прошел регистрацию).
- http://localhost:8000/api/auth/jwt/refresh/ Обновление JWT-токена (Доступно: У кого уже создан токен).
- http://localhost:8000/api/auth/jwt/verify/ Проверка(верификация) JWT-токена (Доступно: У кого уже создан).\
__Реализоана работа с breeds (Работа с породами котов)__
- http://localhost:8000/api/breeds/ GET-list. Получить список всех пород котов
- http://localhost:8000/api/breeds/{id} GET-retrieve. Получить информацию о породе кота по ID. 
- http://localhost:8000/api/breeds/?name= GET. Получение списка котят определенной породы по фильтру: name(имени породы.)\
__Реализоана работа"cats (Работа с породами котов)"__
- http://localhost:8000/api/cats/ GET-list. Получение списка всех котят. 
- http://localhost:8000/api/cats/ POST-create. Добавление информации о котенке. Создание нового кота/кошки.
- http://localhost:8000/api/cats/{id} GET-retrieve. Получение подробной информации о котенке.
- http://localhost:8000/api/cats/{id} PATCH-partial_update. Изменение информации о котенке.
- http://localhost:8000/api/cats/{id} DELETE-destroy. Удаление информации о котенке. \
- http://localhost:8000/api/cats/{id}/photo POST-photo. Добавляет фото к записи кота/кошки по ID кота/кошки.
- __Также написаны загрузчики: 1).Для пользователей; 2).для групп котов, пород котов, котов со всеми атрибутами. 
Заполнить БД нужно в строгой последователности: run python manage.py add_user и poetry run python manage.py cat_db.
Но если вы разворачиваете приложение  помощью Dockera, то это автоматизировано.__
- __Также написаны тесты для всех моделей: test_models.py, которые проверяют работу с помощью моковых данных.__

## 3. Стек технологий <a id=3></a>
[![Django](https://img.shields.io/badge/Django-^4.1.10-6495ED)](https://www.djangoproject.com) 
[![Djangorestframework](https://img.shields.io/badge/djangorestframework-3.14.0-6495ED)](https://www.django-rest-framework.org/) 
[![Authentication wit SimpleJWT](https://img.shields.io/badge/Django_Authentication_with_SimpleJWT-5.2.0-6495ED)](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/getting_started.html)
[![Nginx](https://img.shields.io/badge/Nginx-1.21.3-green)](https://nginx.org/ru/)  
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-blue)](https://www.postgresql.org/)
[![Swagger](https://img.shields.io/badge/Swagger-%201.21.7-blue?style=flat-square&logo=swagger)](https://swagger.io/)
[![Gunicorn](https://img.shields.io/badge/Gunicorn-%2020.0.4-blue?style=flat-square&logo=gunicorn)](https://gunicorn.org/) 
[![Docker](https://img.shields.io/badge/Docker-%2024.0.5-blue?style=flat-square&logo=docker)](https://www.docker.com/)
[![DockerCompose](https://img.shields.io/badge/Docker_Compose-%202.21.0-blue?style=flat-square&logo=docsdotrs)](https://docs.docker.com/compose/)
[![Tested with pytest](https://img.shields.io/badge/Tested_with_pytest-8.1.1-6495ED)](https://docs.pytest.org/en/8.1.x/)

Backend API


## 4. Запуск проекта через docker compose и ссылка на него <a id=4></a>
## Запуск проекта локально в Docker-контейнерах с помощью Docker Compose

Склонируйте проект из репозитория:

```shell
git clone git@github.com:DPavlen/Workmate_cats.git
```

Перейдите в директорию проекта:

```shell
cd Workmate_cats/
```
Ознакомьтесь с .env.example и после этого перейдите в  
корень директории **Workmate_cats/** и создайте файл **.env**:

```shell
nano .env
```

Добавьте строки, содержащиеся в файле **.env.example** и подставьте 
свои значения.

Пример из .env файла:

```dotenv
SECRET_KEY=DJANGO_SECRET_KEY        # Ваш секретный ключ Django
DEBUG=False                         # True - включить Дебаг. Или оставьте пустым для False
IS_LOGGING=False                    # True - включить Логирование. Или оставьте пустым для False
ALLOWED_HOSTS=127.0.0.1 backend     # Список адресов, разделенных пробелами

# Помните, если вы выставляете DEBUG=False, то необходимо будет настроить список ALLOWED_HOSTS.
# 127.0.0.1 и backend является стандартным значением. Через пробел.
# Присутствие backend в ALLOWED_HOSTS обязательно.

В зависимости какую БД нужно запустит:
#DB_ENGINE=sqlite3
DB_ENGINE=postgresql

POSTGRES_USER=django_user                  # Ваше имя пользователя для бд
POSTGRES_PASSWORD=django                   # Ваш пароль для бд
POSTGRES_DB=django                         # Название вашей бд
DB_HOST=db                                 # Стандартное значение - db
DB_PORT=5432                               # Стандартное значение - 5432

```

```shell
В директории **docker** проекта находится файл **docker-compose.yml**, с 
помощью которого вы можете запустить проект локально в Docker контейнерах.
```

Находясь в директории **Workmate_cats/** выполните следующую команду:

> **Примечание.** Если нужно - добавьте в конец команды флаг **-d** для запуска
> в фоновом режиме. Она сбилдит Docker образы и запустит backend django, СУБД PostgreSQL, и Nginx в отдельных Docker контейнерах.
> отработает pytest-1
```shell
sudo docker compose -f docker-compose.yml up --build
```

> **Примечание.** В запущенном контейнер workmate_cats-backend-1 
> активируйте  виртуальное окружение: poetry shell и создайте суперьпользователя
> python manage.py createsuperuser
> Или на эндпойнте http://localhost:8000/api/users/create/ создайте нового пользователя:
> {
>  "email": "user@example.com",
>  "username": "string",
>  "password": "string"
>}

>**Примечание.** Запускаем собраный уже ранее командой:
```shell      
sudo docker compose -f docker-compose.yml up -d**
```

>**Примечание.** Для того чтобы необходимо остановить и удалить контейнер нужно использовать:   
```shell
sudo docker compose -f docker-compose.yml down 
```

По завершении всех операции проект будет запущен и доступен по адресу
http://127.0.0.1/ или http://localhost:8000/ в зависимости от настроек

Либо просто завершите работу Docker Compose в терминале, в котором вы его
запускали, сочетанием клавиш **CTRL+C**.


## 5. Автор проекта: <a id=5></a> 

**Павленко Дмитрий**  
- Ссылка на мой профиль в GitHub [Dmitry Pavlenko](https://github.com/DPavlen)  