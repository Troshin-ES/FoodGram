from djoser.serializers import UserSerializer
from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from recipe.models import (Recipes, FavoriteRecipes, ShoppingLists,
                           Tags, Ingredients, AmountIngredient)
from user.models import CustomUsers, Subscriptions


class CustomUserSerializer(UserSerializer):

    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = CustomUsers
        fields = [
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
        ]

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        author = obj
        if not user.is_authenticated:
            return False
        if Subscriptions.objects.filter(
            author=author,
            follower=user
        ).exists():
            return True
        return False


class SubscriptionsRecipSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipes
        fields = [
            'id',
            'name',
            'image',
            'cooking_time',
            ]


class SubscriptionsSerializer(CustomUserSerializer):

    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = CustomUsers
        fields = [
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count',
        ]

    @staticmethod
    def get_recipes(obj):
        recipes = Recipes.objects.filter(author=obj)
        sub_recipe = SubscriptionsRecipSerializer(data=recipes, many=True)
        sub_recipe.is_valid()
        return sub_recipe.data

    @staticmethod
    def get_recipes_count(obj):
        return Recipes.objects.filter(author=obj).count()


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tags
        fields = [
            'id',
            'name',
            'color',
            'slug'
        ]


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
            'recipe',
            'ingredient',
            'amount'
        ]


class RecipeGET(serializers.ModelSerializer):

    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_list = serializers.SerializerMethodField()
    tags = TagSerializer(many=True)
    author = CustomUserSerializer(required=True)
    print("TYTA")
    # ingredients = AmountIngredientSerializer(many=True, required=True)
    ingredients = serializers.SerializerMethodField()

    class Meta:
        model = Recipes
        fields = [
            'id',
            'tags',
            'author',
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
        # print('get_ingredients')
        # print(obj.id)
        # print(obj)
        ingredient = AmountIngredient.objects.filter(ingredient__recipe=obj)
        ingredient_aaa = AmountIngredient.objects.filter(recipe=obj)
        recipe = AmountIngredient.objects.filter(recipe=obj)
        print(Ingredients.objects.filter)
        print('Ингредиенты')
        print(ingredient)
        print('ingredient_aaa')
        print(ingredient_aaa)
        print('recipe')
        print(recipe)
        # print(ingredient[0].name)
        # serializer = IngredientSerializer(data=ingredient, many=True)
        # print(serializer.is_valid())
        # print()
        # # print(ingredient[0].name)
        # # print(ingredient[0].measurement_unit)
        # print(IngredientSerializer(data=ingredient, many=True))
        # print(IngredientSerializer(data=ingredient, many=True).is_valid())
        # print(IngredientSerializer(data=ingredient).is_valid())
        # print(IngredientSerializer(data=ingredient).data)
    def create(self, validated_data):
        print('create')
