
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


author = CustomUsers(
    email='email@m.ru',
    id=2,
    username='username_author',
    first_name='first_name',
    last_name='last_name',
)


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
        depth = 2

    @staticmethod
    def get_recipes(obj):
        recipes = Recipes.objects.filter(author=obj)
        subscription_recipe = SubscriptionsRecipSerializer(data=recipes, many=True)
        subscription_recipe.is_valid()
        result = []
        for order_dict in subscription_recipe.data:
            result.append(dict(order_dict))
        return result

    def get_recipes_count(self, obj):
        return Recipes.objects.filter(author=obj).count()


def subscriptions(self, request):
    queryset = CustomUsers.objects.filter(author__follower=request.user)
    print(queryset)
    return SubscriptionsSerializer(
        queryset,
        context={'request': request},
        many=True
    ).data


    # res = []
    # for subscription in queryset:
    #     res.append(SubscriptionsSerializer(
    #         subscription.author,
    #         context={'request': request}).data
    #                )
    # return res

def t():
    # subscriptions(None, request)
    return subscriptions(None, request)

# subscriptions = Subscriptions.objects.filter(follower=Request.user)

from t2 import (SubscriptionsSerializer, SubscriptionsRecipSerializer,
                subscriptions, t, Subscriptions)
