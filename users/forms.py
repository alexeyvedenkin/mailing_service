from typing import Any, Dict

from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.forms import BooleanField

from .models import User


class StyleFormMixin:

    fields: Dict[str, Any]

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, BooleanField):
                field.widget.attrs["class"] = "form-check-input"
            else:
                field.widget.attrs["class"] = "form-control"


class UserCreateForm(StyleFormMixin, UserCreationForm):
    phone_number = forms.CharField(max_length=15, required=False, help_text="Необязательное поле. Номер телефона")
    username = forms.CharField(max_length=50, required=True)

    class Meta:
        model = User
        fields = ("email", "username", "phone_number", "country", "password1", "password2")

    def clean_phone_number(self) -> Any:
        phone_number = self.cleaned_data.get("phone_number")
        if phone_number and not phone_number.isdigit():
            raise forms.ValidationError("Номер телефона должен содержать только цифры")
        return phone_number


class CustomAuthenticationForm(StyleFormMixin, AuthenticationForm):
    class Meta:
        model = User
        fields = ("email", "password")


class UserProfileForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = User
        fields = ["email", "phone_number", "avatar", "country"]
