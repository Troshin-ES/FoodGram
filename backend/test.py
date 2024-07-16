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
from api.serializers import RecipeCreateSerializer

t = RecipeCreateSerializer(data=request)
print(t.initial_data)
t.is_valid()
print(t.is_valid())
print(t.errors)
from test import t
