import base64

from django.core.files.base import ContentFile
from djoser.serializers import UserSerializer
from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from recipe.models import (Recipes, FavoriteRecipes, ShoppingLists,
                           Tags, Ingredients, AmountIngredient)
from user.models import CustomUsers, Subscriptions


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        # Если полученный объект строка, и эта строка
        # начинается с 'data:image'...
        if isinstance(data, str) and data.startswith('data:image'):
            # ...начинаем декодировать изображение из base64.
            # Сначала нужно разделить строку на части.
            format, imgstr = data.split(';base64,')
            # И извлечь расширение файла.
            ext = format.split('/')[-1]
            # Затем декодировать сами данные и поместить результат в файл,
            # которому дать название по шаблону.
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


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

    amount = serializers.SerializerMethodField()

    class Meta:
        model = Ingredients
        fields = [
            'id',
            'name',
            'measurement_unit',
            'amount'
        ]

    @staticmethod
    def get_amount(obj):
        return get_object_or_404(AmountIngredient, ingredient=obj).amount


class RecipeSerializer(serializers.ModelSerializer):

    tags = TagSerializer(many=True)
    author = CustomUserSerializer()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_list = serializers.SerializerMethodField()
    image = Base64ImageField()
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
        ingredients = Ingredients.objects.filter(amount__recipe=obj)
        serializer = AmountIngredientSerializer(data=ingredients, many=True)
        serializer.is_valid()
        return serializer.data

    def create(self, validated_data):
        print('create')
