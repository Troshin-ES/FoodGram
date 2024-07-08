from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUsers(AbstractUser):
    email = models.EmailField(
        unique=True,
        max_length=254,
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        ordering = ['username']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class Subscriptions(models.Model):
    "Подписка на автора рецепта"
    author = models.ForeignKey(
        CustomUsers,
        on_delete=models.CASCADE,
        related_name='author',
        verbose_name='Автор рецепта',
    )
    follower = models.ForeignKey(
        CustomUsers,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик',
    )

    class Meta:
        unique_together = ['author', 'follower']
    #     Ограничение не возможно подписаться на самого себя

    def __str__(self):
        return f'Пользователь {self.follower} подписан на {self.author}'

