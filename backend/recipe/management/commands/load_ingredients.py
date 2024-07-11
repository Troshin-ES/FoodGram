import sqlite3
import json

from django.utils.translation import gettext as _
from django.core.management import BaseCommand


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

        for i in data:
            name, measurement_unit = i.values()
            cursor.execute("""
            INSERT INTO recipe_ingredients(name, measurement_unit)
            VALUES(?,?)""", (name, measurement_unit)
                           )
        con.commit()
        con.close()
        print('Загрузка ингредиентов выполнена')
