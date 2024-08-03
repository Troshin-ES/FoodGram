from rest_framework.utils import json

PARAMETERS = {
        'users': {
            'path_file': 'recipe/management/data/users.json',
            'table': 'user_customuser',
            'column_name': (
                'id', 'email', 'username', 'first_name', 'last_name',
                'password', 'is_superuser', 'is_staff', 'is_active',
                'date_joined'
            )
        },
        'tags': {
            'path_file': 'recipe/management/data/tags.json',
            'table': 'recipe_tag',
            'column_name': ('id', 'name', 'color', 'slug')
        },
        'recipes': {
            'path_file': 'recipe/management/data/recipes.json',
            'table': 'recipe_recipe',
            'column_name': (
                'id', 'author_id',
                'name', 'image', 'text', 'cooking_time'
            )
        },
        'recipes_tags': {
            'path_file': 'recipe/management/data/recipes_tags.json',
            'table': 'recipe_recipe_tags',
            'column_name': (
                'id', 'recipe_id', 'tag_id'
            )
        },
        'recipe_amountingredient': {
            'path_file': 'recipe/management/data/recipe_amountingredient.json',
            'table': 'recipe_amountingredient',
            'column_name': (
                'id', 'amount', 'recipe_id', 'ingredient_id'
            )
        }
    }

for i in PARAMETERS:
    path_file = PARAMETERS[i]['path_file']
    with open(path_file, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
    print(data)