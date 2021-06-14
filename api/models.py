import textwrap

from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
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
    genre = models.ManyToManyField(
        Genre,
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


class Review(models.Model):
    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ('-pub_date',)

    FORMAT = (
        'Текст: {text} \n'
        'На произведение: {title}\n'
        'Автор: {author}\n'
        'Дата: {date}'
    )

    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews'
    )

    text = models.TextField(
        blank=False,
        verbose_name='Текст отзыва'
    )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews'
    )

    score = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        verbose_name='Оценка отзыва'
    )

    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата и время написания отзыва'
    )

    def __str__(self):
        return self.FORMAT.format(
            text=textwrap.shorten(self.text, 40),
            title=self.title,
            author=self.author,
            date=self.date.strftime('%b %d %Y %H:%M:%S')
        )


class Comments(models.Model):
    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('-pub_date',)

    FORMAT = (
        'Отзыв: {review}\n'
        'Комментарий: {text}\n'
        'Дата и время создания: {date}\n'
        'Автор: {author}'
    )

    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments'
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
            date=self.pub_date,
            author=self.author
        )
