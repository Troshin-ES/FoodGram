from django.contrib import admin

# Register your models here.
from recipe.models import (Recipes, Tags, Ingredients,
                           FavoriteRecipes, ShoppingLists)

admin.site.register(Recipes)
admin.site.register(Tags)
admin.site.register(Ingredients)
admin.site.register(FavoriteRecipes)
admin.site.register(ShoppingLists)
