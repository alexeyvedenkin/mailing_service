from django.contrib.auth.models import Permission
from django.contrib.auth.decorators import permission_required
from django.http import HttpResponseForbidden
from django.utils.decorators import method_decorator
from django.views import View
from .models import User


class UserPermissions:
    """
    Класс для работы с правами доступа пользователей и менеджеров.
    """

    @staticmethod
    def has_permission(user: User, action: str, object_owner: User) -> bool:
        """
        Проверяет, имеет ли пользователь право выполнять действие над объектом.

        :param user: пользователь, который запрашивает действие
        :param action: действие, которое выполняется ('create', 'view', 'edit', 'delete')
        :param object_owner: владелец объекта (клиент или рассылка)
        :return: True если действие разрешено, иначе False
        """

        if user.is_manager():
            # Менеджеры могут видеть всех
            return action in ['view']

        if user == object_owner:
            # Обычный пользователь может редактировать и удалять только свои объекты
            return action in ['create', 'view', 'edit', 'delete']

        return False