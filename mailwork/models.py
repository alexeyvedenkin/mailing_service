from django.db import models


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

    first_send_time = models.DateTimeField(verbose_name="Дата и время первой отправки", null=True)
    last_send_time = models.DateTimeField(verbose_name="Дата и время последней отправки", null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, verbose_name="Статус", default='created')
    message = models.ForeignKey(Message, on_delete=models.CASCADE, verbose_name="Содержание сообщения")
    recipients = models.ManyToManyField(Recipient, verbose_name="Получатели")

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"
