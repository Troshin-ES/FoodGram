import datetime
from django.core.management import BaseCommand
from user.models import CustomUsers




class Command(BaseCommand):


    def handle(self, *args, **options):
        CustomUsers.objects.create(
            id='1',
            email='admin@m.ru',
            username='admin',
            first_name='first__name_admin',
            last_name='las_name_admin',
            password='admin',
            is_superuser='1',
            is_staff='1',
            is_active='0',
            date_joined=datetime.datetime.today()
        )
        print('Супер пользователь создан')
        print('email: admin@m.ru')
        print('password: admin')
