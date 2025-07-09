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

    def __init__(self, *args, **kwargs):
        super(RecipientForm, self).__init__(*args, **kwargs)

        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Введите email'
        })

        self.fields['fullname'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'username'
        })

        self.fields['comment'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Введите комментарий'
        })


class MessageForm(forms.ModelForm):
    """ Устанавливает параметры формы для создания и редактирования сообщения """
    class Meta:
        model = Message
        fields = [
            "theme",
            "content",
        ]

    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)

        self.fields['theme'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Введите тему сообщения'
        })

        self.fields['content'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Введите текст сообщения'
        })


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
            "message",      # Сообщение для рассылки (ForeignKey)
            "recipients",   # Получатели рассылки (ManyToManyField)
            "first_send_time",  # Дата и время первой отправки
            "last_send_time",   # Дата и времени последней отправки
            "status",       # Статус рассылки
        ]
