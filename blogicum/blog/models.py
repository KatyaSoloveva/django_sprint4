from django.db import models
from django.contrib.auth import get_user_model

from .constants import MAX_LENGTH, LENGTH_LIMIT
from core.models import (CreatedAtModel,
                         IsPublishedCreatedAtModel as PCModel)

User = get_user_model()


class Category(PCModel):
    title = models.CharField('Заголовок', max_length=MAX_LENGTH)
    description = models.TextField('Описание')
    slug = models.SlugField(
        'Идентификатор',
        unique=True,
        help_text='Идентификатор страницы для URL; разрешены '
        'символы латиницы, цифры, дефис и подчёркивание.'
    )

    class Meta():
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title[:LENGTH_LIMIT]


class Location(PCModel):
    name = models.CharField('Название места', max_length=MAX_LENGTH)

    class Meta():
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self):
        return self.name[:LENGTH_LIMIT]


class Post(PCModel):
    title = models.CharField('Заголовок', max_length=MAX_LENGTH)
    text = models.TextField('Текст')
    pub_date = models.DateTimeField(
        'Дата и время публикации',
        help_text='Если установить дату и время в будущем — можно делать '
        'отложенные публикации.'
    )
    image = models.ImageField('Фото', upload_to='post_images', blank=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        verbose_name='Автор публикации'
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Местоположение'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Категория'
    )

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'
        default_related_name = 'posts'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.title[:LENGTH_LIMIT]


class Comment(CreatedAtModel):
    text = models.TextField('Комментария')
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        verbose_name='Пост',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )

    class Meta(CreatedAtModel.Meta):
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии'
        default_related_name = 'comments'

    def __str__(self):
        return self.text[:LENGTH_LIMIT]
