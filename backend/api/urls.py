from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.views import CustomUserViewSet, RecipeViewSet

router = DefaultRouter()

router.register('users', CustomUserViewSet)
router.register('recipes', RecipeViewSet)
# print(router.urls, sep='\n')


urlpatterns = [
    path('', include(router.urls)),
    path(r'', include('djoser.urls')),
    path(r'auth/', include('djoser.urls.authtoken'))
]
