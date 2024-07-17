from rest_framework.exceptions import ValidationError

request = {
  "ingredients": [
    {
      "id": 1123,
      "amount": 10
    },
    {
      "id": 123,
      "amount": 15
    },
    {
      "id": 23,
      "amount": 5
    }
  ],
  "tags": [
    1,
    2
  ],
  "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMAAABieywaAAAACVBMVEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAACklEQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg==",
  "name": "name_recipes_NAME",
  "text": "text_recipes_TEXT",
  "cooking_time": 1
}
# from api.serializers import RecipeCreateSerializer
#
# t = RecipeCreateSerializer(data=request)
# t.is_valid()
# print(t.is_valid())
# print(t.errors)
# print(t.save())
# from test import t


from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
def validators_list(value):
    if value:
        raise ValidationError(
          _("Полу Ингредиенты н может быть пустым")
        )

validators_list([])