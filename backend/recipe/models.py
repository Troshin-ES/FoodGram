from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext as _
from user.models import CustomUsers


class Tags(models.Model):

    name = models.CharField(
        max_length=100,
        verbose_name=_('Название')
    )
    color = models.CharField(
        max_length=7,
        default="#ffffff",
        verbose_name=_('Цвет')
    )
    slug = models.SlugField(
        allow_unicode=True
    )

    class Meta:
        verbose_name = _('Тэг')
        verbose_name_plural = _('Тэги')


class Ingredients(models.Model):
    name = models.CharField(max_length=100)
    measurement_unit = models.CharField(max_length=5)

    class Meta:
        verbose_name = _('Ингредиент')
        verbose_name_plural = _('Ингредиенты')


class Recipes(models.Model):
    tags = models.ForeignKey(
        Tags,
        on_delete=models.CASCADE,
        related_name='recipe',
        verbose_name=_('Тэги')
    )
    author = models.ForeignKey(
        CustomUsers,
        on_delete=models.CASCADE,
        related_name='recipe',
        verbose_name=_('Автор')
    )
    ingredients = models.ForeignKey(
        Ingredients,
        on_delete=models.CASCADE,
        related_name='recipe',
        verbose_name=_('Ингридиенты'),
    )
    name = models.CharField(
        max_length=200,
        verbose_name=_('Название'),
    )
    image = models.ImageField(
        verbose_name=_('Картнка')
    )
    text = models.TextField(
        verbose_name=_('Описание')
    )
    cooking_time = models.IntegerField(
        validators=[
            MinValueValidator(1)
        ],
        verbose_name=_('Время приготовления')
    )

    class Meta:
        verbose_name = _('Рецепт')
        verbose_name_plural = _('Рецепты')

    def __str__(self):
        return f'Название рецепта: {self.name}, автор рецепта: {self.author}'


class FavoriteRecipes(models.Model):
    user = models.ForeignKey(
        CustomUsers,
        on_delete=models.CASCADE,
        related_name='favorite',
        verbose_name=_('Пользователь')
    )
    recipe = models.ForeignKey(
        Recipes,
        on_delete=models.CASCADE,
        related_name='favorite',
        verbose_name=_('Рецепт')
    )

    class Meta:
        verbose_name = _('Избранный рецепт')
        verbose_name_plural = _('Избранные рецепты')


class ShoppingLists(models.Model):
    user = models.ForeignKey(
        CustomUsers,
        on_delete=models.CASCADE,
        related_name='shop_list',
        verbose_name=_('Пользователь')
    )
    recipe = models.ForeignKey(
        Recipes,
        on_delete=models.CASCADE,
        related_name='shop_list',
        verbose_name=_('Рецепт')
    )

    class Meta:
        verbose_name = _('Список покупок')
        verbose_name_plural = _('Списки покупок')
