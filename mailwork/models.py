from typing import Any

from django.core.mail import send_mail
from django.db import models
from django.utils import timezone

from config import settings
from config.settings import DEFAULT_FROM_EMAIL
from users.models import User


class Recipient(models.Model):
    """Определяет параметры модели получателя рассылки"""

    email = models.EmailField(unique=True, verbose_name="Email")
    fullname = models.CharField(max_length=100, verbose_name="ФИО")
    comment = models.TextField(verbose_name="Комментарий", blank=True, null=True)

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Добавлено поле owner

    class Meta:
        verbose_name = "Адресат"
        verbose_name_plural = "Адресаты"
        permissions = [
            ("can_add_recipient", "Может добавлять адресатов"),
            ("can_view_recipient", "Может просматривать адресатов"),
        ]

    def __str__(self) -> str:
        """Определяет формат вывода экземпляра класса Recipient"""
        return f"Адресат: {self.fullname}, email: {self.email}"


class Message(models.Model):
    """Определяет параметры модели сообщения"""

    theme = models.CharField(max_length=100, verbose_name="Тема письма")
    content = models.TextField(verbose_name="Содержание письма")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Владелец")

    class Meta:
        verbose_name = "Письмо"
        verbose_name_plural = "Письма"
        permissions = [
            ("can_send_message", "Может отправлять письма"),
            ("can_view_message", "Может просматривать письма"),
        ]

    def __str__(self) -> str:
        """Определяет формат вывода экземпляра класса Message"""
        return f"Тема сообщения: {self.theme}"


class NewsLetter(models.Model):
    """Определяет параметры модели рассылки"""

    STATUS_CHOICES = [
        ("created", "Создана"),
        ("started", "Запущена"),
        ("completed", "Завершена"),
    ]

    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Владелец")
    first_send_time = models.DateTimeField(verbose_name="Дата и время первой отправки", null=True)
    last_send_time = models.DateTimeField(verbose_name="Дата и время последней отправки", null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, verbose_name="Статус", default="created")
    message = models.ForeignKey(Message, on_delete=models.CASCADE, verbose_name="Содержание сообщения")
    recipients = models.ManyToManyField(Recipient, verbose_name="Получатели")

    @classmethod
    def active_count(cls):
        """Возвращает количество активных рассылок"""
        return cls.objects.filter(status="started").count()

    @classmethod
    def unique_recipient_count(cls):
        """Возвращает количество уникальных получателей"""
        return Recipient.objects.filter(newsletter__status="started").distinct().count()

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"
        permissions = [
            ("can_finish_newsletter", "Может завершать рассылки"),
            ("can_view_newsletter", "Может просматривать рассылки"),
        ]

    def start(self) -> None:
        """Запускает рассылку и устанавливает время первого отправления"""
        if self.status == "created":
            self.first_send_time = timezone.now()  # Устанавливаем текущее время
            self.status = "started"  # Изменяем статус на 'started'
            self.save()  # Сохраняем изменения

    def complete(self) -> None:
        """Завершает рассылку и устанавливает время последней отправки"""
        if self.status in ["created", "started"]:
            self.last_send_time = timezone.now()  # Устанавливаем текущее время
            self.status = "completed"  # Изменяем статус на 'completed'
            self.save()  # Сохраняем изменения

    def get_status_display(self) -> Any:
        """Метод, возвращающий текст статуса"""
        status_dict = dict(self.STATUS_CHOICES)
        return status_dict.get(self.status, self.status)

    def total_attempts(self) -> Any:
        """Подсчет общего количества попыток рассылки для этой рассылки"""
        return SendingAttempt.objects.filter(newsletter=self).count()

    def successful_attempts(self) -> Any:
        """Подсчет количества успешных попыток"""
        return SendingAttempt.objects.filter(newsletter=self, status="success").count()

    def failed_attempts(self) -> Any:
        """Подсчет количества неудачных попыток"""
        return SendingAttempt.objects.filter(newsletter=self, status="failure").count()

    def add_recipient(self, recipient: Recipient) -> None:
        """Добавляет существующего адресата к рассылке"""
        self.recipients.add(recipient)  # Добавляет адресата в ManyToMany поле
        self.save()  # Сохраняет изменения

    def create_and_add_recipient(self, email: str) -> None:
        """Создает нового адресата с заданным email и добавляет его к рассылке"""
        new_recipient = Recipient.objects.create(email=email)  # Создает нового адресата
        self.recipients.add(new_recipient)  # Добавляет нового адресата в рассылку
        self.save()  # Сохраняет изменения


class SendingAttempt(models.Model):
    """Определяет параметры модели попытки рассылки"""

    attempt_time = models.DateTimeField(verbose_name="Дата и время попытки")
    status = models.CharField(
        max_length=15, choices=[("success", "Успешно"), ("failure", "Не успешно")], verbose_name="Статус"
    )
    server_response = models.TextField(verbose_name="Ответ почтового сервера")
    newsletter = models.ForeignKey(NewsLetter, on_delete=models.CASCADE, verbose_name="Рассылка")

    class Meta:
        verbose_name = "Попытка рассылки"
        verbose_name_plural = "Попытки рассылок"

    def __str__(self) -> str:
        """Определяет формат вывода экземпляра класса SendingAttempt"""
        return f"Попытка: {self.attempt_time}, Статус: {self.status}"

    def send_newsletter(self, user: User) -> None:
        """Инициализация отправки рассылки"""
        recipients = self.newsletter.recipients.all()
        for recipient in recipients:
            email = recipient.email
            try:
                # Отправка сообщения
                send_mail(
                    self.newsletter.message.theme,
                    self.newsletter.message.content,
                    from_email=DEFAULT_FROM_EMAIL,
                    recipient_list=[email],
                    fail_silently=False,
                )
                # Если успех, сохраняем попытку
                self.create_attempt("success", "Сообщение успешно отправлено")
            except Exception as e:
                # Если ошибка, сохраняем с текстом ошибки
                self.create_attempt("failure", str(e))

    def create_attempt(self, status: str, response: str) -> None:
        """Создание записи о попытке рассылки"""
        SendingAttempt.objects.create(
            attempt_time=timezone.now(),
            status=status,
            server_response=response,
            newsletter=self.newsletter,
        )
