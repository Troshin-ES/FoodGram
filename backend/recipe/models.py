from django.core.validators import MinValueValidator, validate_slug
from django.db import models
from django.utils.translation import gettext as _

from user.models import CustomUsers


class Tags(models.Model):

    name = models.CharField(
        max_length=100,
        verbose_name=_('Название')
    )
    #поправить цвета
    color = models.CharField(
        max_length=7,
        default="#ffffff",
        verbose_name=_('Цвет')
    )
    slug = models.SlugField(
        allow_unicode=True,
        max_length=200,
        unique=True,
        validators=[validate_slug]
    )

    class Meta:
        verbose_name = _('Тэг')
        verbose_name_plural = _('Тэги')

    def __str__(self):
        return f'{self.name}, slug: {self.slug}'


class Ingredients(models.Model):
    name = models.CharField(max_length=200)
    measurement_unit = models.CharField(max_length=200)

    class Meta:
        verbose_name = _('Ингредиент')
        verbose_name_plural = _('Ингредиенты')

    def __str__(self):
        return f'{self.name}'


class Recipes(models.Model):
    tags = models.ManyToManyField(
        Tags,
        related_name='recipe',
        verbose_name=_('Тэги')
    )
    author = models.ForeignKey(
        CustomUsers,
        on_delete=models.CASCADE,
        related_name='recipe',
        verbose_name=_('Автор')
    )
    ingredients = models.ManyToManyField(
        Ingredients,
        through="AmountIngredient",
        related_name='recipe',
        verbose_name=_('Ингредиенты')
    )
    name = models.CharField(
        max_length=200,
        verbose_name=_('Название'),
    )
    image = models.ImageField(
        upload_to='images',
        null=True,
        default=None,
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


class AmountIngredient(models.Model):
    amount = models.IntegerField(
        validators=[MinValueValidator(1)],
        verbose_name=_('Количество')
    )
    ingredient = models.ForeignKey(
        Ingredients,
        on_delete=models.CASCADE,
        related_name='amount',
        verbose_name=_('Ингредиетн')
    )
    recipe = models.ForeignKey(
        Recipes,
        on_delete=models.CASCADE,
        related_name='amount',
        verbose_name=_('Рецепт')
    )


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
