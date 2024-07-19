from django_filters import rest_framework as filters
from recipe.models import Recipe, Ingredient


class IngredientFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = Ingredient
        fields = ['name']


class RecipeFilter(filters.FilterSet):

    is_favorited = filters.NumberFilter(method='favorite_filter')
    is_in_shopping_cart = filters.NumberFilter(
        method='shopping_cart_filter'
    )
    tags = filters.CharFilter(field_name='tags__slug')
    author = filters.NumberFilter(field_name='author')

    class Meta:
        model = Recipe
        fields = ['author', 'tags', 'is_favorited', 'is_in_shopping_cart']

    def favorite_filter(self, queryset, name, value):
        if value == 1:
            return queryset.filter(favorite__user=self.request.user)
        return queryset

    def shopping_cart_filter(self, queryset, name, value):
        if value == 1:
            return queryset.filter(shop_cart__user=self.request.user)
        return queryset

    @staticmethod
    def tags_filter(queryset, name, value):
        return queryset.filter(tags__slug=value)
