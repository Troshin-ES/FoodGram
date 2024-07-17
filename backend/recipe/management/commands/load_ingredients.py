import sqlite3
import json

from django.utils.translation import gettext as _
from django.core.management import BaseCommand

from recipe.models import Ingredient


class Command(BaseCommand):
    help = _('Загрузка ингредиентов в базу')

    def handle(self, *args, **options):
        con = sqlite3.connect('db.sqlite3')
        cursor = con.cursor()

        with open(
                'recipe/management/data/ingredients.json', 'r',
                encoding='utf-8'
        ) as json_file:
            data = json.load(json_file)
        n = 0
        for i in data:
            n += 1
            cursor.execute("""
            INSERT INTO recipe_ingredient(name, measurement_unit)
            VALUES(?,?)""", tuple(i.values())
                           )
        con.commit()
        con.close()
        print(f'Загружено {n} ингредиентов.')
