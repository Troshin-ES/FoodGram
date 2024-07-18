from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from rest_framework import status, viewsets, filters
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated, \
    IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from api.filters import RecipeFilter
from api.serializers import (SubscriptionsSerializer,
                             TagSerializer,
                             IngredientSerializer, RecipeListSerializer,
                             RecipeCreateSerializer)
from recipe.models import Recipe, Tag, Ingredient, FavoriteRecipe, \
    ShoppingList, AmountIngredient
from user.models import Subscription, CustomUser
from django_filters import rest_framework as filters


class CustomUserViewSet(UserViewSet):
    @action(
        detail=False,
        methods=['GET'],
        permission_classes=[IsAuthenticated]
    )
    def subscriptions(self, request):
        queryset = CustomUser.objects.filter(author__follower=request.user)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = SubscriptionsSerializer(
                page, context={'request': request}, many=True
            )
            return self.get_paginated_response(serializer.data)

        serializer = SubscriptionsSerializer(
            queryset, context={'request': request}, many=True
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=True,
        methods=['POST', 'DELETE'],
        permission_classes=[IsAuthenticated]
    )
    def subscribe(self, request, id):
        author = get_object_or_404(CustomUser, pk=id)
        if request.method == 'POST':
            if author == request.user:
                return Response(
                    {'error': 'Нельзя подписаться на самого себя'},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            obj, created = Subscription.objects.get_or_create(
                author=author,
                follower=request.user
            )
            if created:
                serializer = SubscriptionsSerializer(
                    author, context={'request': request}
                )
                return Response(
                    serializer.data, status=status.HTTP_201_CREATED
                )
            return Response(
                {'error': f'Вы уже подписаны на {author.username}'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if request.method == 'DELETE':
            obj = Subscription.objects.filter(
                author=author,
                follower=request.user
            )
            if obj:
                obj.delete()
                return Response(
                    {'message': f'Вы отписались от {author.username}'},
                    status=status.HTTP_204_NO_CONTENT,
                )
            return Response(
                {'error': f'Вы не подписаны на {author.username}'},
                status=status.HTTP_400_BAD_REQUEST,
            )


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    # filter_backends = [DjangoFilterBackend]
    # filterset_fields = RecipeFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RecipeListSerializer
        if self.request.method in ('POST', 'PATCH'):
            return RecipeCreateSerializer

    @action(
        detail=False,
        methods=['GET'],
        permission_classes=[IsAuthenticated],
    )
    def download_shopping_cart(self, request):
        shop_list_data = ShoppingList.objects.filter(user=request.user)
        with open(
                f'Shopping_cart_{request.user}.txt', 'w', encoding='utf-8'
        ) as file:
            for obj in shop_list_data:
                objects = AmountIngredient.objects.filter(recipe=obj.recipe)
                file.write(f'-=Рецепт: {obj.recipe} =-\n')
                for obj in objects:
                    file.write(f'{obj.ingredient.name}: '
                               f'{obj.amount} '
                               f'{obj.ingredient.measurement_unit}\n')
                file.write(f'{"-"*50}\n')
            return Response(content_type='txt')

    @action(
        detail=True,
        methods=['POST', 'DELETE'],
        permission_classes=[IsAuthenticated],
    )
    def favorite(self, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        if self.request.method == 'POST':
            obj, create = FavoriteRecipe.objects.get_or_create(
                user=request.user,
                recipe=recipe
            )
            if create:
                return Response(
                    f'Рецепт {recipe} добавлен в избранное.',
                    status=status.HTTP_201_CREATED
                )
            return Response(
                f'Рецепт {recipe} уже есть в избранном.',
                status=status.HTTP_400_BAD_REQUEST
            )
        if self.request.method == 'DELETE':
            obj = FavoriteRecipe.objects.filter(
                user=self.request.user, recipe=recipe
            )
            if obj:
                obj.delete()
                return Response(
                    f'Рецепт {recipe} успешно удален из избранного.',
                    status=status.HTTP_204_NO_CONTENT
                )
            return Response(
                f'Рецепт {recipe} не добавлен в избранное.',
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(
        detail=True,
        methods=['POST', 'DELETE'],
        permission_classes=[IsAuthenticated]
    )
    def shopping_cart(self, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        if self.request.method == 'POST':
            obj, create = ShoppingList.objects.get_or_create(
                user=request.user,
                recipe=recipe
            )
            if create:
                return Response(
                    f'Рецепт {recipe} добавлен в список покупок.',
                    status=status.HTTP_201_CREATED
                )
            return Response(
                f'Рецепт {recipe} уже есть в списке покупок.',
                status=status.HTTP_400_BAD_REQUEST
            )
        if self.request.method == 'DELETE':
            obj = ShoppingList.objects.filter(
                user=self.request.user, recipe=recipe
            )
            if obj:
                obj.delete()
                return Response(
                    f'Рецепт {recipe} успешно удален из списка покупок.',
                    status=status.HTTP_204_NO_CONTENT
                )
            return Response(
                f'Рецепт {recipe} не добавлен в список покупок.',
                status=status.HTTP_400_BAD_REQUEST
            )


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer

