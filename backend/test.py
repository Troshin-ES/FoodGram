from rest_framework import serializers

from api.serializers import UserSerializer, CustomUsers
from recipe.models import Recipes
from user.models import Subscriptions


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


class request:
    user = CustomUsers.objects.get(pk=1)
    # user = CustomUsers(
    #     email='admin@m.ru',
    #     id=1,
    #     username='admin',
    #     first_name='admin',
    #     last_name='admin',
    # )


author = CustomUsers(
    email='email@m.ru',
    id=2,
    username='username_author',
    first_name='first_name',
    last_name='last_name',
)

serializer = CustomUserSerializer(author, context={'request': Request})


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
    recipes_count = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()

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

    def get_recipes_count(self, obj):
        return Subscriptions.objects.filter(
            follower=self.context['request'].user
        ).count()

    def get_recipes(self, obj):
        print(obj)
        subscriptions = Subscriptions.objects.filter(
            follower=self.context['request'].user
        )
        ser_recipe = []
        for subscription in subscriptions:
            recipes = Recipes.objects.filter(author=subscription.author)
            sub_recipe = SubscriptionsRecipSerializer(data=recipes, many=True)
            sub_recipe.is_valid()
            ser_recipe.append(dict(sub_recipe.data[0]))
        return ser_recipe

print(request.user)


# subscriptions = Subscriptions.objects.filter(follower=Request.user)

# recipes = []
# for subscription in subscriptions:
#     # print(subscription.author)  # авторы
#     # print(Recipes.objects.filter(author=subscription.author)) # список рецептов автора#
#     recipes = Recipes.objects.filter(author=subscription.author)
#     # print(SubscriptionsRecipSerializer(recipes))
#     ser_recipe = SubscriptionsRecipSerializer(data=recipes, many=True)
#     ser_recipe.is_valid()
#     print(ser_recipe.data)

# def get_recipes():
#     ser_recipe = []
#     for subscription in subscriptions:
#         recipes = Recipes.objects.filter(author=subscription.author)
#         recipe = SubscriptionsRecipSerializer(data=recipes, many=True)
#         # print(recipe)
#         recipe.is_valid()
#         # print(recipe.data)
#         return recipe.data
#         # ser_recipe.append(recipe.data.values())
#     # return ser_recipe

# r = get_recipes()

# r1 = Recipes.objects.get(pk=1)
# r1_a = Recipes.objects.filter(author=3)
# SubscriptionsRecipSerializer(r1_a, many=True)
# print('Рецепт')
# print(r1)
# print('Сериализатор')
# print(SubscriptionsRecipSerializer(r1))
#
# r1_s = SubscriptionsRecipSerializer(r1)
#
# sub_ser = SubscriptionsSerializer(Request.user,
#                                   context={'request': Request}
#                                   , many=True)


# from test import (
#     UserSerializer, CustomUsers, CustomUserSerializer, SubscriptionsRecipSerializer,
#     Recipes, sub_ser, r,
#     Request, serializer, author,
# )

