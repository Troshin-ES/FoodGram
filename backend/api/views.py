from djoser.views import UserViewSet
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.response import Response

from api.serializers import SubscriptionsSerializer, CustomUserSerializer
from user.models import Subscriptions, CustomUsers


class CustomUserViewSet(UserViewSet):
    @action(
        detail=False,
        methods=['get', 'post', 'delete'],
        pagination_class=PageNumberPagination
    )
    def subscriptions(self, request):

        queryset = Subscriptions.objects.filter(
            follower=request.user
        )
        result = []
        for subscription in queryset:
            author = subscription.author
            result.append(SubscriptionsSerializer(author, context={'request': request}).data)
        return Response(data=result)

