import os

import psycopg2
import json

from django.utils.translation import gettext as _
from django.core.management import BaseCommand


class Command(BaseCommand):
    help = _('Загрузка ингредиентов в базу')

    def handle(self, *args, **options):
        conn = psycopg2.connect(
            dbname=os.getenv('POSTGRES_DB'),
            user=os.getenv('POSTGRES_USER'),
            password=os.getenv('POSTGRES_PASSWORD'),
            host=os.getenv('DB_HOST')
        )
        cursor = conn.cursor()

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
            VALUES(%s,%s)""", tuple(i.values())
                           )
        conn.commit()
        conn.close()
        print(f'Загружено {n} ингредиентов.')
