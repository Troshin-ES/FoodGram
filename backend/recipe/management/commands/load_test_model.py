import datetime
import sqlite3
import json

from django.utils.translation import gettext as _
from django.core.management import BaseCommand

from recipe.models import Recipes, Tags
from user.models import CustomUsers


class Command(BaseCommand):

    PARAMETERS = {
        # 'users': {'path_file': 'recipe/management/data/users.json',
        #           'table': 'user_customusers',
        #           'column_name': (
        #               'id', 'email', 'username', 'first_name', 'last_name',
        #               'password', 'is_superuser', 'is_staff', 'is_active',
        #               'date_joined')
        #           },
        # 'tags': {
        #     'path_file': 'recipe/management/data/tags.json',
        #     'table': 'recipe_tags',
        #     'column_name': ('id', 'name', 'color', 'slug')
        # },
        'recipes': {
            'path_file': 'recipe/management/data/recipes.json',
            'table': 'recipe_recipes',
            'column_name': (
                'id', 'tags_id', 'author_id', 'ingredients_id',
                'name', 'image', 'text', 'cooking_time'
            )
        }
    }

    help = _('Загрузка пользователей в базу')
    con = sqlite3.connect('db.sqlite3')
    cursor = con.cursor()

    def load(self, path_file, table, column_name):
        with open(path_file, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
        for i in data:
            print(i)
            if table == 'recipe_recipes':
                Recipes.objects.create(
                    id=i['id'],
                    tags_id=i['tags_id'],
                    author_id=i['author_id'],
                    ingredients_id=i['ingredients_id'],
                    name=i['name'],
                    image=i['image'],
                    text=i['text'],
                    cooking_time=i['cooking_time']
                )
            # if table ==

    def handle(self, *args, **options):
        for i in self.PARAMETERS:
            print(f'Добавления записей в {self.PARAMETERS[i]["table"]}')
            # try:

            self.load(
                self.PARAMETERS[i]['path_file'],
                self.PARAMETERS[i]['table'],
                self.PARAMETERS[i]['column_name']
            )
            print('Выполнено')
            # except:
            #     print(
            #         'Ошибка во время добавления в '
            #         f'{self.PARAMETERS[i]["table"]}'
            #     )

    @staticmethod
    def load_user_customusers(i):
        CustomUsers.objects.create(
            id=i['id'],
            email=i['email'],
            username=i['username'],
            first_name=i['first_name'],
            lasn_name=i['last_name'],
            password=i['password'],
            is_superuser=i['is_superuser'],
            is_staff=i['is_staff'],
            is_active=i['is_active'],
            date_joined=i['date_joined']
        )

    @staticmethod
    def load_recipe_tags(i):
        Tags.objects.create(
            id=i['id'],
            name=i['name'],
            color=i['color'],
            slug=i['slug']
        )

    @staticmethod
    def load_recipe_recipes(i):
        Recipes.objects.create(
            id=i['id'],
            tags_id=i['tags_id'],
            author_id=i['author_id'],
            ingredients_id=i['ingredients_id'],
            name=i['name'],
            image=i['image'],
            text=i['text'],
            cooking_time=i['cooking_time']
        )

    # @staticmethod
    # def load_recipe_recipes_tags(i):
    #     Recipes.objects.create(
    #         id=i['id'],
    #         recipe_id=i['recipe_id'],
    #         tags_id=i['tags_id']
    #     )

    @staticmethod
    def load_recipe_amount_ingredient():
        pass

