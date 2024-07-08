from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext as _
from user.models import CustomUsers


class Tags(models.Model):
    pass


class Ingredients(models.Model):
    pass


class Recipes(models.Model):
    tags = models.ForeignKey(
        Tags,
        on_delete=models.CASCADE,
        related_name='recipe'
    )
    author = models.ForeignKey(
        CustomUsers,
        on_delete=models.CASCADE,
        related_name='recipe'
    )
    ingredients = models.ForeignKey(
        Ingredients,
        on_delete=models.CASCADE,
        related_name='recipe'
    )
    name = models.CharField(
        max_length=200
    )
    image = models.ImageField()
    text = models.TextField()
    cooking_time = models.IntegerField(
        validators=[
            MinValueValidator(1)
        ]
    )

    def __str__(self):
        return f'Название рецепта: {self.name}, автор рецепта: {self.author}'
