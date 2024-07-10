from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny, IsAuthenticated
from rest_framework.response import Response

from api.serializers import SubscriptionsSerializer, CustomUserSerializer
from user.models import Subscriptions, CustomUsers


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
