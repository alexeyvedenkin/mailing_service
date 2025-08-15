from typing import Tuple

from django.contrib import admin

from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display: Tuple[str, str, str, str, str, str] = (
        "id",
        "email",
        "username",
        "phone_number",
        "country",
        "get_groups",
    )
    list_filter: Tuple[str] = ("country",)
    search_fields: Tuple[str] = ("username",)

    @admin.display(description="Группы")  # Используем декоратор для описания
    def get_groups(self, obj: User) -> str:
        """Группирует объекты типа User"""
        return ", ".join([group.name for group in obj.groups.all()])

    get_groups.short_description = "Группы"
