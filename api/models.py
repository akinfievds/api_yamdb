import textwrap

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from api.validators import year_validator
from users.models import User


class Category(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Название категории',
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Идентификатор категории',
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('pk', )

    def __str__(self) -> str:
        return self.name


class Genre(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Название жанра',
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Идентификатор жанра',
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ('pk', )

    def __str__(self) -> str:
        return self.name


class Title(models.Model):
    FORMAT = (
        'Название произведения: {name}\n'
        'Описание произведения: {description}\n'
        'Год выпуска: {year}\n'
        'Жанр: {genre}\n'
        'Категория: {category}\n'
    )
    name = models.CharField(
        max_length=200,
        db_index=True,
        verbose_name='Название произведения',
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='Описание произведения',
    )
    year = models.PositiveSmallIntegerField(
        blank=True,
        validators=[year_validator],
        verbose_name='Год выпуска произведения',
    )
    genre = models.ManyToManyField(
        Genre,
        blank=True,
        related_name='titles',
        verbose_name='Жанр',
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='titles',
        verbose_name='Категория',
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ('-id', )

    def __str__(self):
        description = self.description
        if not self.description:
            description = '...'
        return self.FORMAT.format(
            name=self.name,
            description=textwrap.shorten(description, 40),
            year=self.year,
            genre=self.genre,
            category=self.category,
        )


class Review(models.Model):
    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ('-pub_date', )

    FORMAT = (
        'Текст: {text} \n'
        'На произведение: {title}\n'
        'Автор: {author}\n'
        'Дата: {date}'
    )
    SCORE_OVER_RANGE_MSG = 'Оценка отзыва может быть в диапазоне от 1 до 10'

    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        null=True
    )

    text = models.TextField(
        blank=False,
        verbose_name='Текст отзыва'
    )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        null=True
    )

    score = models.IntegerField(
        validators=[
            MinValueValidator(1, message=SCORE_OVER_RANGE_MSG),
            MaxValueValidator(10, message=SCORE_OVER_RANGE_MSG)
        ],
        verbose_name='Оценка отзыва'
    )

    pub_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name='Дата и время написания отзыва'
    )

    def __str__(self):
        return self.FORMAT.format(
            text=textwrap.shorten(self.text, 40),
            title=self.title,
            author=self.author,
            date=self.pub_date.strftime('%b %d %Y %H:%M:%S')
        )


class Comments(models.Model):
    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('-pub_date', )

    FORMAT = (
        'Отзыв: {review}\n'
        'Комментарий: {text}\n'
        'Дата и время создания: {date}\n'
        'Автор: {author}'
    )

    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        null=True
    )

    text = models.TextField(
        blank=False,
        verbose_name='Текст комментария'
    )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )

    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата и время добавления комментария'
    )

    def __str__(self):
        return self.FORMAT.format(
            review=self.review,
            text=textwrap.shorten(self.text, 40),
            date=self.pub_date.strftime('%b %d %Y %H:%M:%S'),
            author=self.author
        )
