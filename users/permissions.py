from .models import User


class UserPermissions:
    """
    Класс для работы с правами доступа пользователей и менеджеров.
    """

    @staticmethod
    def has_permission(user: User, action: str, object_owner: User) -> bool:
        """ Проверяет, имеет ли пользователь право выполнять действие над объектом """

        if user.is_manager():
            # Менеджеры могут видеть всех
            return action in ['view']

        if user == object_owner:
            # Обычный пользователь может редактировать и удалять только свои объекты
            return action in ['create', 'view', 'edit', 'delete']

        return False
