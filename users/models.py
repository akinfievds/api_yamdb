from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    USER = 'USER'
    ADMIN = 'ADMIN'
    MODERATOR = 'MODERATOR'
    ADMIN_DJANGO = 'ADMIN_DJANGO'

    ROLES_CHOICES = [
        (USER, 'user'),
        (ADMIN, 'admin'),
        (MODERATOR, 'moderator'),
        (ADMIN_DJANGO, 'admin_django'),
    ]
    password = None
    bio = models.CharField(max_length=300, blank=True)
    role = models.CharField(
        max_length=12,
        choices=ROLES_CHOICES,
        default=USER
    )
