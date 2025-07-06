from django.core.management.base import BaseCommand
from mailwork.models import NewsLetter, SendingAttempt
from users.models import User


class Command(BaseCommand):
    help = 'Отправляет рассылку вручную'

    def handle(self, *args, **options):
        # Здесь можно реализовать логику для выбора рассылки
        newsletter = NewsLetter.objects.first()  # Например, берем первую рассылку
        if newsletter:
            attempt = SendingAttempt(newsletter=newsletter)
            attempt.send_newsletter(User.objects.first())  # Передаем первого пользователя
            self.stdout.write(self.style.SUCCESS('Рассылка успешно отправлена!'))
        else:
            self.stdout.write(self.style.ERROR('Нет доступных рассылок'))
