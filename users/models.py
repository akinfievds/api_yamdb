import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    class UserRole:
        USER = 'user'
        ADMIN = 'admin'
        MODERATOR = 'moderator'
        choices = [
            (USER, 'user'),
            (ADMIN, 'admin'),
            (MODERATOR, 'moderator'),
        ]

    email = models.EmailField(
        unique=True,
        verbose_name='Электронная почта'
    )
    bio = models.CharField(
        max_length=300,
        blank=True,
        verbose_name='Информация о пользователе'
    )
    role = models.CharField(
        max_length=12,
        choices=UserRole.choices,
        default=UserRole.USER
    )
    confirmation_code = models.UUIDField(
        default=uuid.uuid4,
        editable=False
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
