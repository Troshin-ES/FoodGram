import base64

from django.core.files.base import ContentFile
from rest_framework import serializers, viewsets

from api.serializers import TagSerializer
from recipe.models import FavoriteRecipes, ShoppingLists, Recipes, \
    AmountIngredient, Ingredients
from user.models import CustomUsers


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredients
        fields = [
            'id',
            'name',
            'measurement_unit'
        ]


class AmountIngredientSerializer(serializers.ModelSerializer):
    #
    # id =
    # name =
    # measurement_unit =
    class Meta:
        model = AmountIngredient
        fields = [
            'id',
            'name',
            'measurement_unit',
            'amount'
        ]


class RecipeGET(serializers.ModelSerializer):

    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_list = serializers.SerializerMethodField()
    tags = TagSerializer(many=True, required=False)
    print("TYTA")
    # ingredients = AmountIngredientSerializer(many=True, required=True)
    ingredients = serializers.SerializerMethodField()

    class Meta:
        model = Recipes
        fields = [
            'id',
            'tags',
            # 'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_list',
            'name',
            'image',
            'text',
            'cooking_time'
        ]

    def get_is_favorited(self, obj):
        user = self.context['request'].user
        recipe = obj
        if not user.is_authenticated:
            return False
        if FavoriteRecipes.objects.filter(
                recipe=recipe,
                user=user
        ).exists():
            return True
        return False

    def get_is_in_shopping_list(self, obj):
        user = self.context['request'].user
        recipe = obj
        if not user.is_authenticated:
            return False
        if ShoppingLists.objects.filter(
                recipe=recipe,
                user=user
        ).exists():
            return True
        return False

    def get_ingredients(self, obj):
        print('get_ingredients')
        print(obj)
        ingredient = AmountIngredient.objects.filter(recipe__ingredient=obj)
        print(ingredient)



class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        # Если полученный объект строка, и эта строка
        # начинается с 'data:image'...
        if isinstance(data, str) and data.startswith('data:image'):
            # ...начинаем декодировать изображение из base64.
            # Сначала нужно разделить строку на части.
            format, imgstr = data.split(';base64,')
            # И извлечь расширение файла.
            ext = format.split('/')[-1]
            # Затем декодировать сами данные и поместить результат в файл,
            # которому дать название по шаблону.
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


class RecipeCreateSerializer(serializers.ModelSerializer):

    image = Base64ImageField()
    ingredients = serializers.SerializerMethodField()
    class Meta:
        model = Recipes
        fields = [
            'ingredients',
            'tags',
            'image',
            'name',
            'text',
            'cooking_time'
        ]


    def get_ingredients(self):
        print(self.data)
        AmountIngredient.objects.create(
            recipe='',
            ingredient='',
            amount=''
        )

    def create(self, validated_data):
        print(**validated_data)

request = {
  "ingredients": [
    {
      "id": 1123,
      "amount": 10
    }
  ],
  "tags": [
    1,
    2
  ],
  "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMAAABieywaAAAACVBMVEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAACklEQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg==",
  "name": "string",
  "text": "string",
  "cooking_time": 1
}
r = Recipes.objects.create()
