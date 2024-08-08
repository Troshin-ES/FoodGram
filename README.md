 
# Продуктовый помощник Foodgram 

[![Python](https://img.shields.io/badge/-Python-464646?style=flat&logo=Python&logoColor=56C0C0&color=008080)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat&logo=Django&logoColor=56C0C0&color=008080)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?style=flat&logo=Django%20REST%20Framework&logoColor=56C0C0&color=008080)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat&logo=PostgreSQL&logoColor=56C0C0&color=008080)](https://www.postgresql.org/)
[![Nginx](https://img.shields.io/badge/-NGINX-464646?style=flat&logo=NGINX&logoColor=56C0C0&color=008080)](https://nginx.org/ru/)
[![gunicorn](https://img.shields.io/badge/-gunicorn-464646?style=flat&logo=gunicorn&logoColor=56C0C0&color=008080)](https://gunicorn.org/)
[![Docker](https://img.shields.io/badge/-Docker-464646?style=flat&logo=Docker&logoColor=56C0C0&color=008080)](https://www.docker.com/)
[![Docker-compose](https://img.shields.io/badge/-Docker%20compose-464646?style=flat&logo=Docker&logoColor=56C0C0&color=008080)](https://www.docker.com/)
[![Docker Hub](https://img.shields.io/badge/-Docker%20Hub-464646?style=flat&logo=Docker&logoColor=56C0C0&color=008080)](https://www.docker.com/products/docker-hub)

## Описание проекта Foodgram
«Продуктовый помощник»: приложение, на котором пользователи публикуют рецепты, 
подписываться на публикации других авторов и добавлять рецепты в избранное. 
Сервис «Список покупок» позволит пользователю создавать список продуктов, 
которые нужно купить для приготовления выбранных блюд.

## Запуск проекта через Docker

Установите и запустите Docker, используя инструкции с официального сайта:
- для [Windows и MacOS](https://www.docker.com/products/docker-desktop)
- для [Linux](https://docs.docker.com/engine/install/ubuntu/). Отдельно потребуется установть [Docker Compose](https://docs.docker.com/compose/install/)

Клонируйте репозиторий с проектом на свой компьютер.

```bash
git clone https://github.com/Troshin-ES/FoodGram.git
```

- Создать файл .env в папке проекта:
```.env
DB_NAME=postgres # имя базы данных
POSTGRES_USER=postgres # логин для подключения к базе данных
POSTGRES_PASSWORD=postgres # пароль для подключения к БД

DB_HOST=db # название сервиса
DB_PORT=5432 # порт для подключения к БД

DEBUG=False # отключите режим отладки 
DJANGO_SECRET = '***' # укажите секретный ключ django 

ALLOWED_HOSTS = '' # ip-адрес сервера
```
Выполните команды:
```bash
cd .\FoodGram\
docker-compose up -d --build
```

- В результате должны быть собрано три контейнера, при введении следующей команды получаем список запущенных контейнеров:  
```bash
docker-compose ps
```
Назначение контейнеров:  

| NAMES               |        DESCRIPTIONS         |
|:--------------------|:---------------------------:|
| foodgram-nginx-1    |   контейнер HTTP-сервера    |
| foodgram-db_1       |    контейнер базы данных    |
| foodgram-backend_1  | контейнер приложения Django |


### Выполните миграции:
```bash
docker-compose exec backend python manage.py migrate
```

### Загрузите статику:
```bash
docker-compose exec backend python manage.py collectstatic --no-input
```

### Заполните базу тестовыми данными:
```bash
docker-compose exec backend python manage.py load_ingredients
docker-compose exec backend python manage.py load_test_data   
```
### Создайте суперпользователя:
```bash
docker-compose exec backend python manage.py createsuperuser
```

### Основные адреса: 

| Адрес               | Описание |
|:--------------------|:---------|
| localhost           | Главная страница |
| localhost/admin/    | Для входа в панель администратора |
| localhost/api/docs/ | Описание работы API |

## Пользовательские роли
| Функционал                                                                                                                | Неавторизованные пользователи |  Авторизованные пользователи | Администратор  |
|:--------------------------------------------------------------------------------------------------------------------------|:---------:|:---------:|:---------:|
| Доступна главная страница.                                                                                                | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |
| Доступна и работает форма авторизации                                                                                     | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |
| Доступна страница отдельного рецепта.                                                                                     | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |
| Доступна и работает форма регистрации.                                                                                    | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |
| Доступна страница «Мои подписки»                                                                                          | :x: | :heavy_check_mark: | :heavy_check_mark: |
| Можно подписаться и отписаться на странице рецепта                                                                        | :x: | :heavy_check_mark: | :heavy_check_mark: |
| Можно подписаться и отписаться на странице автора                                                                         | :x: | :heavy_check_mark: | :heavy_check_mark: |
| При подписке рецепты автора добавляются на страницу «Мои подписки» и удаляются оттуда при отказе от подписки.             | :x: | :heavy_check_mark: | :heavy_check_mark: |
| Доступна страница «Избранное»                                                                                             | :x: | :heavy_check_mark: | :heavy_check_mark: |
| На странице рецепта есть возможность добавить рецепт в список избранного и удалить его оттуда                             | :x: | :heavy_check_mark: | :heavy_check_mark: |
| На любой странице со списком рецептов есть возможность добавить рецепт в список избранного и удалить его оттуда           | :x: | :heavy_check_mark: | :heavy_check_mark: |
| Доступна страница «Список покупок»                                                                                        | :x: | :heavy_check_mark: | :heavy_check_mark: |
| На странице рецепта есть возможность добавить рецепт в список покупок и удалить его оттуда                                | :x: | :heavy_check_mark: | :heavy_check_mark: |
| На любой странице со списком рецептов есть возможность добавить рецепт в список покупок и удалить его оттуда              | :x: | :heavy_check_mark: | :heavy_check_mark: |
| Есть возможность выгрузить файл (.txt) с перечнем и количеством необходимых ингредиентов для рецептов из «Списка покупок» | :x: | :heavy_check_mark: | :heavy_check_mark: |
| Ингредиенты в выгружаемом списке не повторяются, корректно подсчитывается общее количество для каждого ингредиента        | :x: | :heavy_check_mark: | :heavy_check_mark: |
| Доступна страница «Создать рецепт»                                                                                        | :x: | :heavy_check_mark: | :heavy_check_mark: |
| Есть возможность опубликовать свой рецепт                                                                                 | :x: | :heavy_check_mark: | :heavy_check_mark: |
| Есть возможность отредактировать и сохранить изменения в своём рецепте                                                    | :x: | :heavy_check_mark: | :heavy_check_mark: |
| Есть возможность удалить свой рецепт                                                                                      | :x: | :heavy_check_mark: | :heavy_check_mark: |
| Доступна и работает форма изменения пароля                                                                                | :x: | :heavy_check_mark: | :heavy_check_mark: |
| Доступна возможность выйти из системы (разлогиниться)                                                                     | :x: | :heavy_check_mark: | :heavy_check_mark: |
| Доступна и работает система восстановления пароля.                                                                        | :x: | :heavy_check_mark: | :heavy_check_mark: |
| Изменять пароль любого пользователя.                                                                                      | :x: | :x: | :heavy_check_mark: |
| Создавать/блокировать/удалять аккаунты пользователей.                                                                     | :x: | :x: | :heavy_check_mark: |
| Редактировать/удалять любые рецепты.                                                                                      | :x: | :x: | :heavy_check_mark: |
| Добавлять/удалять/редактировать ингредиенты.                                                                              | :x: | :x: | :heavy_check_mark: |
| Добавлять/удалять/редактировать теги.                                                                                     | :x: | :x: | :heavy_check_mark: |


### Автор:  
_Трошин Евгений_<br>
**email**: _troshin-es@mail.ru_<br>
**telegram** __ 