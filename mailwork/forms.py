from django import forms
from .models import Message, NewsLetter, Recipient
from django.core.exceptions import ValidationError
from PIL import Image


class RecipientForm(forms.ModelForm):
    class Meta:
        model = Recipient
        fields = [
            "email",
            "fullname",
            "comment",
        ]

class MessageForm(forms.ModelForm):
    pass
    # class Meta:
    #     model = Recipient
    #     fields = [
    #         "email",
    #         "fullname",
    #         "comment",
    #     ]

class NewsLetterForm(forms.ModelForm):
    pass
    # class Meta:
    #     model = Recipient
    #     fields = [
    #         "email",
    #         "fullname",
    #         "comment",
    #     ]
