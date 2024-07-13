import datetime
import sqlite3
import json

from django.utils.translation import gettext as _
from django.core.management import BaseCommand

from user.models import CustomUsers


class Command(BaseCommand):

    PARAMETERS = {
        'users': {'path_file': 'recipe/management/data/users.json',
                  'table': 'user_customusers',
                  'column_name': (
                      'id', 'email', 'username', 'first_name', 'last_name',
                      'password', 'is_superuser', 'is_staff', 'is_active',
                      'date_joined')
                  },
        'tags': {
            'path_file': 'recipe/management/data/tags.json',
            'table': 'recipe_tags',
            'column_name': ('id', 'name', 'color', 'slug')
        },
        'recipes': {
            'path_file': 'recipe/management/data/recipes.json',
            'table': 'recipe_recipes',
            'column_name': (
                'id', 'author_id',
                'name', 'image', 'text', 'cooking_time'
            )
        },
        'recipes_tags': {
            'path_file': 'recipe/management/data/recipes_tags.json',
            'table': 'recipe_recipes_tags',
            'column_name': (
                'id', 'recipes_id', 'tags_id'
            )
        },
        'recipes_ingredients': {
            'path_file': 'recipe/management/data/recipes_ingredients.json',
            'table': 'recipe_recipes_ingredients',
            'column_name': (
                'id', 'recipes_id', 'ingredients_id'
            )
        }
    }

    help = _('Загрузка тестовых данных в базу')
    con = sqlite3.connect('db.sqlite3')
    cursor = con.cursor()

    def load(self, path_file, table, column_name):
        with open(path_file, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
        for i in data:
            self.cursor.execute(
                f"""INSERT INTO {table}{column_name}
                VALUES({'?,' * (len(column_name)-1) + '?'})""", tuple(i.values())
            )

    def handle(self, *args, **options):
        for i in self.PARAMETERS:
            try:
                print(f'Таблица {self.PARAMETERS[i]["table"]} очищена')
                self.cursor.execute(
                    f"""DELETE FROM {self.PARAMETERS[i]['table']}"""
                )
                print(f'Добавления записей в {self.PARAMETERS[i]["table"]}')
                self.load(
                    self.PARAMETERS[i]['path_file'],
                    self.PARAMETERS[i]['table'],
                    self.PARAMETERS[i]['column_name']
                )
                self.con.commit()
                print('Выполнено')
            except sqlite3.IntegrityError:
                print(
                    'Ошибка во время добавления в ' 
                    f'{self.PARAMETERS[i]["table"]}'
                )
        self.con.close()

        self.create_superuser()

    @staticmethod
    def create_superuser():
        CustomUsers.objects.create_user(
            id=1,
            email='admin@m.ru',
            username='admin',
            first_name='first__name_admin',
            last_name='las_name_admin',
            password='admin',
            is_superuser=1,
            is_staff=1,
            is_active=1,
            date_joined=datetime.datetime.today()
        )
        print('Супер пользователь создан')
        print('email: admin@m.ru')
        print('password: admin')
