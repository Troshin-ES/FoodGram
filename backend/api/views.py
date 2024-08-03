from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django_filters import rest_framework as filters
from api.filters import RecipeFilter, IngredientFilter
from api.paginations import CustomPagination
from api.permissions import IsAuthorOrReadOnly
from api.serializers import (SubscriptionsSerializer,
                             TagSerializer,
                             IngredientSerializer, RecipeListSerializer,
                             RecipeCreateSerializer,
                             FavoriteAndShopCartSerializer)
from recipe.models import (Recipe, Tag, Ingredient, FavoriteRecipe,
                           ShoppingCart, AmountIngredient)
from user.models import Subscription, CustomUser


class CustomUserViewSet(UserViewSet):
    pagination_class = CustomPagination
    @action(
        detail=False,
        methods=['GET'],
        permission_classes=[IsAuthenticated]
    )
    def subscriptions(self, request):
        """Список авторов на которых подписан пользователь"""
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
        """Подписка на автора рецепта"""
        author = get_object_or_404(CustomUser, pk=id)
        if request.method == 'POST':
            if author == request.user:
                return Response(status=status.HTTP_400_BAD_REQUEST)
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
            return Response(status=status.HTTP_400_BAD_REQUEST)
        if request.method == 'DELETE':
            obj = Subscription.objects.filter(
                author=author,
                follower=request.user
            )
            if obj:
                obj.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(status=status.HTTP_400_BAD_REQUEST)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = [IsAuthorOrReadOnly]
    pagination_class = CustomPagination
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
        """Скачать лист покупок"""
        queryset = AmountIngredient.objects.filter(
            recipe__shop_cart__user=request.user
        ).values(
            'ingredient__name',
            'ingredient__measurement_unit'
        ).annotate(sum=Sum('amount'))
        shopping_list = ''
        for i in queryset:
            shopping_list += (f'{i["ingredient__name"]}: '
                              f'{i["sum"]} '
                              f'{i["ingredient__measurement_unit"]}\n')
        return HttpResponse(shopping_list, content_type='text/plain')

    @action(
        detail=True,
        methods=['POST', 'DELETE'],
        permission_classes=[IsAuthenticated],
    )
    def favorite(self, request, pk):
        """Добавление рецепта в избранное"""
        return self.method_post_and_delete(request, pk, FavoriteRecipe)

    @action(
        detail=True,
        methods=['POST', 'DELETE'],
        permission_classes=[IsAuthenticated]
    )
    def shopping_cart(self, request, pk):
        """Добавление в список покупок"""
        return self.method_post_and_delete(request, pk, ShoppingCart)

    def method_post_and_delete(self, request, pk, model):
        """Метод добавления и удаления в список покупок или избранное,
        с проверкой дублирования и наличия"""
        recipe = get_object_or_404(self.queryset, pk=pk)
        if request.method == 'POST':
            obj, create = model.objects.get_or_create(
                user=request.user,
                recipe=recipe
            )
            if create:
                serializer = FavoriteAndShopCartSerializer(recipe)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        if request.method == 'DELETE':
            obj = model.objects.filter(user=request.user, recipe=recipe)
            if obj:
                obj.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(status=status.HTTP_400_BAD_REQUEST)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [AllowAny]


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = IngredientFilter
