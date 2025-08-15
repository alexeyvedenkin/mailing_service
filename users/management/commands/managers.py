from typing import Any

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractBaseUser):  # Создаем CustomUser, расширяя базовый класс
    email = models.EmailField(unique=True)  # Поле для электронной почты
    username = models.CharField(max_length=255)  # Поле для имени пользователя
    # Добавьте другие поля и настройки, необходимые для вашего пользователя

    USERNAME_FIELD = "email"  # Указываем, что email будет использоваться для аутентификации
    REQUIRED_FIELDS = ["username"]  # Указываем обязательные поля


class CustomUserManager(BaseUserManager):
    """Кастомный менеджер моделей, в котором электронная почта является уникальным идентификатором
    для аутентификации вместо имени пользователя"""

    def create_user(self, email: str, username: str, password: str, **extra_fields: Any) -> Any:
        """Создает и сохраняет пользователя с указанным адресом электронной почты и паролем"""
        if not email:
            raise ValueError(_("Необходимо указать e-mail"))
        if not username:
            raise ValueError(_("Username is required"))
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user
