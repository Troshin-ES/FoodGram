from djoser.serializers import UserSerializer
from rest_framework.response import Response
from rest_framework import serializers

from recipe.models import Recipes
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
