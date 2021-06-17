import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    class UserRole:
        USER = 'user'
        ADMIN = 'admin'
        MODERATOR = 'moderator'
        options = [
            (USER, 'user'),
            (ADMIN, 'admin'),
            (MODERATOR, 'moderator')
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
        max_length=25,
        choices=UserRole.options,
        default=UserRole.USER
    )
    confirmation_code = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        null=True
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
