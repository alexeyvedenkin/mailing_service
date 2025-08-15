import secrets
from typing import Any

from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.views import LoginView
from django.core.mail import send_mail
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView

from config.settings import EMAIL_HOST_USER

from .forms import CustomAuthenticationForm, UserCreateForm, UserProfileForm
from .models import User


def manager_required(function: Any) -> Any:
    """Проверка на то, что пользователь - менеджер"""
    return user_passes_test(lambda u: u.is_authenticated and u.is_manager)(function)


@manager_required
def user_list(request: HttpRequest) -> HttpResponse:
    """Представление для просмотра списка пользователей"""
    users = User.objects.all()  # Получаем всех пользователей
    return render(request, "users/user_list.html", {"users": users})


@manager_required
def block_user(request: HttpRequest, user_id: int) -> HttpResponse:
    """Представление для блокировки пользователя"""
    user = get_object_or_404(User, id=user_id)
    user.is_active = False  # Блокируем пользователя
    user.save()
    return redirect("users:user_list")  # Перенаправление на список пользователей


class RegisterView(CreateView):
    """Контроллер для доступа к форме регистрации пользователя"""

    model = User
    template_name = "users/register.html"
    form_class = UserCreateForm
    success_url = reverse_lazy("users:login")

    def form_valid(self, form: UserCreateForm) -> HttpResponse:
        """Обработка валидной формы регистрации пользователя"""
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f"http://{host}/users/email-confirm/{token}/"
        send_mail(
            subject="Подтверждение почты",
            message=f"Привет, перейди по ссылке для подтверждения регистрации {url}",
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email],
        )
        return super().form_valid(form)


def email_verification(request: Any, token: str) -> Any:
    """Метод для проверки email пользователя по токену"""

    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse("users:login"))


class CustomLoginView(LoginView):
    """Контроллер для доступа к форме аутентификации пользователя"""

    authentication_form = CustomAuthenticationForm
    template_name = "users/login.html"


@login_required
def edit_profile(request: HttpRequest) -> HttpResponse:
    user = request.user
    if request.method == "POST":
        form = UserProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect("profile_success")
    else:
        form = UserProfileForm(instance=user)
    return render(request, "edit_profile.html", {"form": form})


class ProfileSuccessView(TemplateView):
    """Контроллер для доступа сохранения обновленных данных пользователя"""

    template_name = "users/profile_success.html"

    def get_context_data(self, **kwargs: Any) -> Any:
        context = super().get_context_data(**kwargs)
        context["message"] = "Ваш профиль успешно обновлен!"
        return context


class EditProfileView(View):
    """Контроллер для доступа к форме обновления данных пользователя"""

    def get(self, request: HttpRequest) -> HttpResponse:
        form = UserProfileForm(instance=request.user)  # Предполагая, что у вас есть форма
        return render(request, "users/edit_profile.html", {"form": form})

    def post(self, request: HttpRequest) -> HttpResponse:
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("users:profile_success")  # Убедитесь, что используете именование с пространством
        return render(request, "users/templates/edit_profile.html", {"form": form})
