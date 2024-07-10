from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomUsers(AbstractUser):
    email = models.EmailField(
        unique=True,
        max_length=254,
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        ordering = ['username']
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return self.username


class Subscriptions(models.Model):
    "Подписка на автора рецепта"
    author = models.ForeignKey(
        CustomUsers,
        on_delete=models.CASCADE,
        related_name='author',
        verbose_name=_('Автор рецепта'),
    )
    follower = models.ForeignKey(
        CustomUsers,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name=_('Подписчик'),
    )

    class Meta:
        verbose_name = _('Подписчик')
        verbose_name_plural = _('Подписчики')
        unique_together = ['author', 'follower']

    def __str__(self):
        return f'Пользователь {self.follower} подписан на {self.author}'

