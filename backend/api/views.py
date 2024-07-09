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
    def subscribe(self, request, id=None):
        print('self')
        print(self)
        print(dir(self))
        print()
        print('request')
        print(request)
        print(dir(request))
        pass