from django.contrib import admin
from .models import CustomUser, Subscription
# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Subscription)
