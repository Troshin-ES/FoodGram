from rest_framework import serializers, viewsets

from api.serializers import TagSerializer
from recipe.models import FavoriteRecipes, ShoppingLists, Recipes, \
    AmountIngredient, Ingredients
from user.models import CustomUsers


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredients
        fields = [
            'id',
            'name',
            'measurement_unit'
        ]


class AmountIngredientSerializer(serializers.ModelSerializer):
    #
    # id =
    # name =
    # measurement_unit =
    class Meta:
        model = AmountIngredient
        fields = [
            'id',
            'name',
            'measurement_unit',
            'amount'
        ]


class RecipeGET(serializers.ModelSerializer):

    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_list = serializers.SerializerMethodField()
    tags = TagSerializer(many=True, required=False)
    print("TYTA")
    # ingredients = AmountIngredientSerializer(many=True, required=True)
    ingredients = serializers.SerializerMethodField()

    class Meta:
        model = Recipes
        fields = [
            'id',
            'tags',
            # 'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_list',
            'name',
            'image',
            'text',
            'cooking_time'
        ]

    def get_is_favorited(self, obj):
        user = self.context['request'].user
        recipe = obj
        if not user.is_authenticated:
            return False
        if FavoriteRecipes.objects.filter(
                recipe=recipe,
                user=user
        ).exists():
            return True
        return False

    def get_is_in_shopping_list(self, obj):
        user = self.context['request'].user
        recipe = obj
        if not user.is_authenticated:
            return False
        if ShoppingLists.objects.filter(
                recipe=recipe,
                user=user
        ).exists():
            return True
        return False

    def get_ingredients(self, obj):
        print('get_ingredients')
        print(obj)
        ingredient = AmountIngredient.objects.filter(recipe__ingredient=obj)
        print(ingredient)


request = Recipes.objects.all()
r = RecipeGET(request)

from t3_recipe import r
