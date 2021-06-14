from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Category(models.Model):
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    name = models.CharField(
        max_length=200,
        verbose_name='Название категории',
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Идентификатор категории',
    )

    def __str__(self) -> str:
        return self.name


class Genre(models.Model):
    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    name = models.CharField(
        max_length=200,
        verbose_name='Название жанра',
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Идентификатор жанра',
    )

    def __str__(self) -> str:
        return self.name


class Title(models.Model):
    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ('-year',)

    FORMAT = (
        'Название произведения: {name}\n'
        'Описание произведения: {description}\n'
        'Год выпуска: {year}\n'
        'Жанр: {genre}\n'
        'Категория: {category}\n'
    )
    name = models.CharField(
        max_length=200,
        verbose_name='Название произведения',
    )
    description = models.TextField(
        blank=True,
        verbose_name='Описание произведения',
    )
    year = models.IntegerField(
        blank=True,
        verbose_name='Год выпуска произведения',
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='genres',
        verbose_name='Жанр',
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='categories',
        verbose_name='Категория',
    )

    def __str__(self):
        return self.FORMAT.format(
            name=self.name,
            description=self.description[:40],
            year=self.year,
            genre=self.genre,
            category=self.category,
        )
