from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Команда для создания администратора"""

    def handle(self, *args: str, **options: dict) -> None:
        User = get_user_model()
        user = User.objects.create(
            email="testadmin@sky.pro",
            first_name="Admin",
            last_name="Admin",
        )

        user.set_password("1234")

        user.is_active = True
        user.is_staff = True
        user.is_superuser = True

        user.save()

        self.stdout.write(self.style.SUCCESS(f"Successfully created admin user with email {user.email}"))
