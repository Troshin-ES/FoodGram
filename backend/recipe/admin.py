from django.contrib import admin

# Register your models here.
from recipe.models import (Recipe, Tag, Ingredient,
                           FavoriteRecipe, ShoppingList,
                           AmountIngredient)

admin.site.register(Recipe)
admin.site.register(Tag)
admin.site.register(Ingredient)
admin.site.register(FavoriteRecipe)
admin.site.register(ShoppingList)
admin.site.register(AmountIngredient)
