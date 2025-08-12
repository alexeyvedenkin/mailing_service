from django import forms
from django.core.exceptions import ValidationError

from .models import Message, NewsLetter, Recipient


class RecipientForm(forms.ModelForm):
    """Устанавливает параметры формы для создания и редактирования адресата"""

    class Meta:
        model = Recipient
        fields = [
            "email",
            "fullname",
            "comment",
        ]

    def __init__(self, *args, **kwargs):
        super(RecipientForm, self).__init__(*args, **kwargs)

        self.fields["email"].widget.attrs.update({"class": "form-control", "placeholder": "Введите email"})

        self.fields["fullname"].widget.attrs.update({"class": "form-control", "placeholder": "username"})

        self.fields["comment"].widget.attrs.update({"class": "form-control", "placeholder": "Введите комментарий"})


class MessageForm(forms.ModelForm):
    """Устанавливает параметры формы для создания и редактирования сообщения"""

    class Meta:
        model = Message
        fields = [
            "theme",
            "content",
        ]

    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)

        self.fields["theme"].widget.attrs.update({"class": "form-control", "placeholder": "Введите тему сообщения"})

        self.fields["content"].widget.attrs.update({"class": "form-control", "placeholder": "Введите текст сообщения"})

    # Пример валидации
    def clean_body(self):
        content = self.cleaned_data.get("content")
        if len(content) < 10:  # Пример валидации длины
            raise ValidationError("Сообщение должно содержать минимум 10 символов.")
        return content


class NewsLetterForm(forms.ModelForm):
    new_recipient_email = forms.EmailField(
        required=False,
        label="Новый адресат",
        widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "Введите email нового адресата"}),
    )

    recipients = forms.ModelMultipleChoiceField(
        queryset=Recipient.objects.all(),  # Получаем всех получателей
        widget=forms.CheckboxSelectMultiple,  # Используем чекбоксы для выбора
        required=False,
    )  # Добавляем виджет для выбора адресатов

    class Meta:
        model = NewsLetter
        fields = [
            "message",
            "recipients",
            "status",
        ]

    def __init__(self, *args, **kwargs):
        super(NewsLetterForm, self).__init__(*args, **kwargs)

        # Добавляем классы для стиля
        self.fields["message"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Введите сообщение для рассылки"}
        )

    def clean(self):
        """Метод для обработки нового адресата"""
        cleaned_data = super().clean()
        new_email = cleaned_data.get("new_recipient_email")

        # Если введен новый email, добавляем его в модель Recipient
        if new_email:
            # Создаем нового адресата и добавляем его к получателям
            recipient, created = Recipient.objects.get_or_create(email=new_email)
            # Добавляем нового адресата в выбор получателей
            cleaned_data["recipients"].add(recipient)

        return cleaned_data  # Возвращаем очищенные данные
