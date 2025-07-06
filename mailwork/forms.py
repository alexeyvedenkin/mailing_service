from django import forms
from .models import Message, NewsLetter, Recipient
from django.core.exceptions import ValidationError
from PIL import Image


class RecipientForm(forms.ModelForm):
    """ Устанавливает параметры формы для создания и редактирования адресата"""
    class Meta:
        model = Recipient
        fields = [
            "email",
            "fullname",
            "comment",
        ]


class MessageForm(forms.ModelForm):
    """ Устанавливает параметры формы для создания и редактирования сообщения """
    class Meta:
        model = Message
        fields = [
            "theme",
            "content",
        ]

    # Пример валидации
    def clean_body(self):
        content = self.cleaned_data.get("content")
        if len(content) < 10:  # Пример валидации длины
            raise ValidationError("Сообщение должно содержать минимум 10 символов.")
        return content


class NewsLetterForm(forms.ModelForm):
    """ Форма для создания или редактирования рассылки. """
    class Meta:
        model = NewsLetter  # Указываем модель для связи с формой
        fields = [
            "theme",        # Тема рассылки
            "message",      # Сообщение для рассылки (ForeignKey)
            "recipients",   # Получатели рассылки (ManyToManyField)
            "first_send_time",  # Дата и время первой отправки
            "last_send_time",   # Дата и времени последней отправки
            "status",       # Статус рассылки
        ]
