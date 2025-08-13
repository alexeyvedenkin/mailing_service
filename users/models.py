from typing import Any

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Класс для работы с моделью пользователя"""

    email = models.EmailField(unique=True, verbose_name="Email")
    phone_number = models.CharField(max_length=15, verbose_name="Телефон", blank=True, null=True)
    avatar = models.ImageField(upload_to="users/avatars/", verbose_name="Аватар", blank=True, null=True)
    country = models.CharField(max_length=25, verbose_name="Страна", blank=True, null=True)

    token = models.CharField(max_length=100, verbose_name="Token", blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
        "username",
    ]

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        permissions = [
            ("can_block_user", "Может блокировать пользователя"),
            ("can_view_users", "Может просматривать список пользователей"),
        ]

    def __str__(self) -> Any:
        return self.email
