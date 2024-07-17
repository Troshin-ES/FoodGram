import base64

from django.core.files.base import ContentFile
from djoser.serializers import UserSerializer
from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from api.validations import validate_list
from recipe.models import (Recipe, FavoriteRecipe, ShoppingList,
                           Tag, Ingredient, AmountIngredient)
from user.models import CustomUser, Subscription


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
        model = CustomUser
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
        if Subscription.objects.filter(
            author=author,
            follower=user
        ).exists():
            return True
        return False


class SubscriptionsRecipSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
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
        model = CustomUser
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
        recipes = Recipe.objects.filter(author=obj)
        sub_recipe = SubscriptionsRecipSerializer(data=recipes, many=True)
        sub_recipe.is_valid()
        return sub_recipe.data

    @staticmethod
    def get_recipes_count(obj):
        return Recipe.objects.filter(author=obj).count()


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = [
            'id',
            'name',
            'color',
            'slug'
        ]


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = [
            'id',
            'name',
            'measurement_unit'
        ]


class AmountIngredientSerializer(serializers.ModelSerializer):

    amount = serializers.SerializerMethodField()

    class Meta:
        model = Ingredient
        fields = [
            'id',
            'name',
            'measurement_unit',
            'amount'
        ]

    # @staticmethod
    def get_amount(self, obj):
        return get_object_or_404(
            AmountIngredient,
            recipe=self.context['recipe'],
            ingredient=obj
        ).amount


class RecipeListSerializer(serializers.ModelSerializer):

    tags = TagSerializer(many=True)
    author = CustomUserSerializer()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_list = serializers.SerializerMethodField()
    image = Base64ImageField()
    ingredients = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
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
        if FavoriteRecipe.objects.filter(
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
        if ShoppingList.objects.filter(
                recipe=recipe,
                user=user
        ).exists():
            return True
        return False

    @staticmethod
    def get_ingredients(obj):
        ingredients = Ingredient.objects.filter(amount__recipe=obj)
        serializer = AmountIngredientSerializer(
            data=ingredients, context={'recipe': obj}, many=True
        )
        serializer.is_valid()
        return serializer.data


class AmountIngredientCreateSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=True)
    amount = serializers.IntegerField(min_value=1)


class RecipeCreateSerializer(serializers.ModelSerializer):
    ingredients = AmountIngredientCreateSerializer(
        many=True,
        required=True
    )
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = [
            'ingredients',
            'tags',
            'image',
            'name',
            'text',
            'cooking_time'
        ]

    @staticmethod
    def processing_of_ingredient(recipe, ingredients_data):
        for ingredient_data in ingredients_data:
            AmountIngredient.objects.create(
                recipe=recipe,
                ingredient=get_object_or_404(
                    Ingredient, pk=ingredient_data['id']
                ),
                amount=ingredient_data['amount']
            )

    def create(self, validated_data):
        ingredients_data = validated_data.pop('ingredients')
        tags_data = validated_data.pop('tags')
        recipe = Recipe.objects.create(
                author=self.context['request'].user,
                **validated_data
        )
        recipe.tags.add(*tags_data)
        self.processing_of_ingredient(recipe, ingredients_data)
        return recipe

    def update(self, instance, validated_data):
        ingredients_data = validated_data.pop('ingredients')
        self.processing_of_ingredient(instance, ingredients_data)
        instance.tags.add(*validated_data.pop('tags'))
        instance.image = validated_data.get('image', instance.image)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get(
            'cooking_time', instance.cooking_time
        )
        instance.save()
        return instance

    def to_representation(self, instance):
        return RecipeListSerializer(
            instance,
            context={'request': self.context['request']}
        ).data
