from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.views import (CustomUserViewSet, RecipeViewSet,
                       TagViewSet, IngredientViewSet)

router = DefaultRouter()

router.register('users', CustomUserViewSet, basename='users')
router.register('recipes', RecipeViewSet, basename='recipes')
router.register('tags', TagViewSet, basename='tags')
router.register('ingredients', IngredientViewSet, basename='ingredients')


urlpatterns = [
    path('', include(router.urls)),
    path(r'auth/', include('djoser.urls.authtoken'))
]

