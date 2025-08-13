from typing import Any

from django.core.mail import send_mail
from django.db import models
from django.utils import timezone

from config.settings import DEFAULT_FROM_EMAIL
from users.models import User


class Recipient(models.Model):
    """Определяет параметры модели получателя рассылки"""

    email = models.EmailField(unique=True, verbose_name="Email")
    fullname = models.CharField(max_length=100, verbose_name="ФИО")
    comment = models.TextField(verbose_name="Комментарий", blank=True, null=True)

    class Meta:
        verbose_name = "Адресат"
        verbose_name_plural = "Адресаты"

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

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"

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

    @classmethod
    def overall_statistics(cls) -> Any:
        """Получение общей статистики по всем рассылкам"""
        try:
            total_newsletters = cls.objects.count()  # Общее количество рассылок
            total_attempts = SendingAttempt.objects.count()  # Общее количество попыток
            successful_attempts = SendingAttempt.objects.filter(status="success").count()  # Успешные попытки
            failed_attempts = SendingAttempt.objects.filter(status="failure").count()  # Неудачные попытки

            return {
                "total_newsletters": total_newsletters,
                "total_attempts": total_attempts,
                "successful_attempts": successful_attempts,
                "failed_attempts": failed_attempts,
            }
        except Exception as e:
            print(f"Ошибка: {e}")  # Выводим ошибку в консоль
            return {  # Возвращаем пустые значения вместо None
                "total_newsletters": 0,
                "total_attempts": 0,
                "successful_attempts": 0,
                "failed_attempts": 0,
            }

    def get_newsletter_info(self) -> Any:
        """Получение информации о состоянии всех полей рассылки"""
        # Формируем информацию о рассылке

        # Получаем всех получателей
        recipients_list = self.recipients.all()  # Изменено: получаем список всех получателей

        info = {
            "owner": self.owner.id,
            "first_send_time": self.first_send_time,
            "last_send_time": self.last_send_time,
            "status": self.get_status_display(),  # Используем метод для отображения статуса
            "message": self.message.content,  # Содержимое сообщения
            "recipients_count": len(recipients_list),  # Теперь используем количество получателей из списка
            "recipients_emails": [recipient.email for recipient in recipients_list],  # Получаем emails
        }

        # Вывод информации на консоль
        print("Информация о рассылке:")
        for key, value in info.items():
            print(f"{key}: {value}")  # Выводим ключ и его значение

        return info  # Возвращаем информацию о рассылке

    # Метод для добавления существующего адресата
    def add_recipient(self, recipient: Recipient) -> None:
        """Добавляет существующего адресата к рассылке"""
        self.recipients.add(recipient)  # Добавляет адресата в ManyToMany поле
        self.save()  # Сохраняет изменения

    # Метод для создания и добавления нового адресата
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

    def send_newsletter(self, user: User) -> None:  # Добавляем параметр user
        """Инициализация отправки рассылки"""
        recipients = self.newsletter.recipients.all()  # type: ignore
        for recipient in recipients:
            email = recipient.email  # email экземпляра Recipient
            try:
                # Отправка сообщения
                send_mail(
                    self.newsletter.message.theme,  # type: ignore
                    self.newsletter.message.content,  # type: ignore
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
        SendingAttempt.objects.create(  # type: ignore
            attempt_time=timezone.now(),  # type: ignore
            status=status,
            server_response=response,
            newsletter=self.newsletter,
        )
