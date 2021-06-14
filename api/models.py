from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Category(models.Model):
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(models.Model):
    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
