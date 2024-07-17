from django_filters import rest_framework as filters
from recipe.models import Recipe


class SlugFilter(filters.CharFilter):
    pass


class RecipeFilter(filters.FilterSet):

    is_favorited = filters.NumberFilter(field_name='is_favorited')
    is_in_shopping_list = filters.NumberFilter(field_name='is_in_shopping_list')
    tags = SlugFilter(field_name='tags__slug', lookup_expr='icontains')

    class Meta:
        model = Recipe
        fields = ['tags', 'author']
