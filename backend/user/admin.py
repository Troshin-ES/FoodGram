from django.contrib import admin
from .models import CustomUsers, Subscriptions
# Register your models here.
admin.site.register(CustomUsers)
admin.site.register(Subscriptions)
