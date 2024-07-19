from django.http import FileResponse
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from django_filters import rest_framework as filters
from api.filters import RecipeFilter, IngredientFilter
from api.serializers import (SubscriptionsSerializer,
                             TagSerializer,
                             IngredientSerializer, RecipeListSerializer,
                             RecipeCreateSerializer)
from api.view_managment import method_post_and_delete
from recipe.models import (Recipe, Tag, Ingredient, FavoriteRecipe,
                           ShoppingCart, AmountIngredient)
from user.models import Subscription, CustomUser


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
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = RecipeFilter

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
        shop_list_data = ShoppingCart.objects.filter(user=request.user)
        with open(
                f'media/shop_lists/Shopping_cart.txt',
                'w',
                encoding='utf-8'
        ) as file:
            for obj in shop_list_data:
                objects = AmountIngredient.objects.filter(recipe=obj.recipe)
                file.write(f'-=Рецепт: {obj.recipe} =-\n')
                for obj in objects:
                    file.write(f'{obj.ingredient.name}: '
                               f'{obj.amount} '
                               f'{obj.ingredient.measurement_unit}\n')
                file.write(f'{"-"*50}\n')
        return FileResponse(open(
            f'media/shop_lists/Shopping_cart.txt',
            'r',
            encoding='utf-8').read(),
                            as_attachment=True,
                            filename='Список покупок.txt',
                            )

    @action(
        detail=True,
        methods=['POST', 'DELETE'],
        permission_classes=[IsAuthenticated],
    )
    def favorite(self, request, pk):
        return method_post_and_delete(
            self.queryset, request, pk, FavoriteRecipe
        )

    @action(
        detail=True,
        methods=['POST', 'DELETE'],
        permission_classes=[IsAuthenticated]
    )
    def shopping_cart(self, request, pk):
        return method_post_and_delete(self.queryset, request, pk, ShoppingCart)


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = IngredientFilter
