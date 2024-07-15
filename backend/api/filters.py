from django_filters import rest_framework as filters
from recipe.models import Recipes


class RecipeFilter(filters.FilterSet):

    is_favorited = filters.BooleanFilter(field_name='is_favorited')
    is_in_shopping_list = filters.BooleanFilter(field_name='is_in_shopping_list')

    class Meta:
        model = Recipes
        fields = ['tags', 'author']
