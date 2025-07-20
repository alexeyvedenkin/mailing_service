from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    """
    Кастомный менеджер моделей, в котором электронная почта является уникальным идентификатором
    для аутентификации вместо имени пользователя.
    """
    def create_user(self, email, username, password, **extra_fields):
        """
        Создает и сохраняет пользователя с указанным адресом электронной почты и паролем.
        """
        if not email:
            raise ValueError(_("Необходимо указать e-mail"))
        if not username:
            raise ValueError(_("Username is required"))
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user
