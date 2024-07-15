from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from rest_framework import status, viewsets, filters
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from api.filters import RecipeFilter
from api.serializers import (SubscriptionsSerializer, CustomUserSerializer,
                             RecipeSerializer, TagSerializer,
                             IngredientSerializer)
from recipe.models import Recipes, Tags, Ingredients
from user.models import Subscriptions, CustomUsers
from django_filters import rest_framework as filters

class CustomUserViewSet(UserViewSet):
    @action(
        detail=False,
        methods=['get'],
        permission_classes=[IsAuthenticated]
    )
    def subscriptions(self, request):
        queryset = CustomUsers.objects.filter(author__follower=request.user)
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
        methods=['post', 'delete'],
        permission_classes=[IsAuthenticated]
    )
    def subscribe(self, request, id):
        author = get_object_or_404(CustomUsers, pk=id)
        if request.method == 'POST':
            if author == request.user:
                return Response(
                    {'error': 'Нельзя подписаться на самого себя'},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            obj, created = Subscriptions.objects.get_or_create(
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
            obj = Subscriptions.objects.filter(
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


# class RecipeViewSet(viewsets.ViewSet):
#     permission_classes = [AllowAny]
#     # filter_backends = []
#
#     @staticmethod
#     def list(request):
#         queryset = Recipes.objects.all()
#         serializer = RecipeSerializer(
#             queryset, context={'request': request}, many=True
#         )
#         return Response(serializer.data)


class RecipeViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    filter_backends = [filters.DjangoFilterBackend]
    # search_fields = ['author__id', 'tags']
    # filterset_fields = ['is_favorited', 'is_in_shopping_list', 'id__author']
    filterset_fields = RecipeFilter

    def get_queryset(self):
        if self.request.method == 'GET':
            return Recipes.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RecipeSerializer(
                self.get_queryset(),
                context={'request': self.request},
                many=True
            )

    def list(self, request, *args, **kwargs):
        return Response(self.get_serializer_class().data)


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tags.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredients.objects.all()
    serializer_class = IngredientSerializer

