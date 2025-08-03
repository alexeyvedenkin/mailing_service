from datetime import timezone

from django.core.mail import send_mail
from django.db import models

from users.models import User


class Recipient(models.Model):
    """ Определяет параметры модели получателя рассылки """
    email = models.EmailField(unique=True, verbose_name="Email")
    fullname = models.CharField(max_length=100, verbose_name="ФИО")
    comment = models.TextField(verbose_name="Комментарий", blank=True, null=True)

    class Meta:
        verbose_name = "Адресат"
        verbose_name_plural = "Адресаты"

    def __str__(self) -> str:
        """ Определяет формат вывода экземпляра класса Recipient """
        return f"Адресат: {self.fullname}, email: {self.email}"


class Message(models.Model):
    """ Определяет параметры модели сообщения """
    theme = models.CharField(max_length=100, verbose_name="Тема письма")
    content = models.TextField(verbose_name="Содержание письма")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Владелец", default=1)

    class Meta:
        verbose_name = "Письмо"
        verbose_name_plural = "Письма"

    def __str__(self) -> str:
        """ Определяет формат вывода экземпляра класса Message """
        return f"Тема сообщения: {self.theme}"


class NewsLetter(models.Model):
    """ Определяет параметры модели рассылки """
    STATUS_CHOICES = [
        ('created', 'Создана'),
        ('started', 'Запущена'),
        ('completed', 'Завершена'),
    ]

    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Владелец", default=1)
    first_send_time = models.DateTimeField(verbose_name="Дата и время первой отправки", null=True)
    last_send_time = models.DateTimeField(verbose_name="Дата и время последней отправки", null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, verbose_name="Статус", default='created')
    message = models.ForeignKey(Message, on_delete=models.CASCADE, verbose_name="Содержание сообщения")
    recipients = models.ManyToManyField(Recipient, verbose_name="Получатели")

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"

    def get_status_display(self):
        """ Метод, возвращающий текст статуса """
        status_dict = dict(self.STATUS_CHOICES)
        return status_dict.get(self.status, self.status)

    def total_attempts(self):
        """ Подсчет общего количества попыток рассылки для этой рассылки """
        return SendingAttempt.objects.filter(newsletter=self).count()

    def successful_attempts(self):
        """ Подсчет количества успешных попыток """
        return SendingAttempt.objects.filter(newsletter=self, status='success').count()

    def failed_attempts(self):
        """ Подсчет количества неудачных попыток """
        return SendingAttempt.objects.filter(newsletter=self, status='failure').count()

    @classmethod
    def overall_statistics(cls):
        """ Получение общей статистики по всем рассылкам """
        total_newsletters = cls.objects.count()  # Общее количество рассылок
        total_attempts = SendingAttempt.objects.count()  # Общее количество попыток
        successful_attempts = SendingAttempt.objects.filter(status='success').count()  # Успешные попытки
        failed_attempts = SendingAttempt.objects.filter(status='failure').count()  # Неудачные попытки

        return {
            'total_newsletters': total_newsletters,
            'total_attempts': total_attempts,
            'successful_attempts': successful_attempts,
            'failed_attempts': failed_attempts,
        }


class SendingAttempt(models.Model):
    """ Определяет параметры модели попытки рассылки """
    attempt_time = models.DateTimeField(verbose_name="Дата и время попытки")
    status = models.CharField(max_length=15, choices=[('success', 'Успешно'), ('failure', 'Не успешно')], verbose_name="Статус")
    server_response = models.TextField(verbose_name="Ответ почтового сервера")
    newsletter = models.ForeignKey(NewsLetter, on_delete=models.CASCADE, verbose_name="Рассылка")

    class Meta:
        verbose_name = "Попытка рассылки"
        verbose_name_plural = "Попытки рассылок"

    def __str__(self) -> str:
        """ Определяет формат вывода экземпляра класса SendingAttempt """
        return f"Попытка: {self.attempt_time}, Статус: {self.status}"

    def send_newsletter(self, user: User):  # Добавляем параметр user
        """ Инициализация отправки рассылки """
        recipients = self.newsletter.recipients.all()  # type: ignore
        for recipient in recipients:
            email = recipient.email  # email экземпляра Recipient
            try:
                # Отправка сообщения
                send_mail(
                    self.newsletter.message.theme,  # type: ignore
                    self.newsletter.message.content,  # type: ignore
                    user.email,  # email экземпляра User
                    [email],
                    fail_silently=False,
                )
                # Если успех, сохраняем попытку
                self.create_attempt('success', 'Сообщение успешно отправлено')
            except Exception as e:
                # Если ошибка, сохраняем с текстом ошибки
                self.create_attempt('failure', str(e))

    def create_attempt(self, status, response):
        """ Создание записи о попытке рассылки """
        SendingAttempt.objects.create(  # type: ignore
            attempt_time=timezone.now(),    # type: ignore
            status=status,
            server_response=response,
            newsletter=self.newsletter
        )
