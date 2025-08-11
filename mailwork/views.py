from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages  # Импортируем для отображения сообщений
from django.core.exceptions import ValidationError
from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    TemplateView,
    UpdateView,
)

from mailwork.forms import RecipientForm, MessageForm, NewsLetterForm
from mailwork.models import Message, NewsLetter, Recipient, SendingAttempt
from datetime import datetime  # Импортируем datetime для работы с временем


class RecipientListView(LoginRequiredMixin, ListView):
    """ Контроллер для отображения списка получателей """
    model = Recipient
    context_object_name = "recipients"
    template_name = "mailwork/recipients_list.html"

class RecipientCreateView(LoginRequiredMixin, CreateView):
    """ Контроллер для создания экземпляра класса Recipient """
    model = Recipient
    form_class = RecipientForm
    template_name = 'mailwork/recipient_form.html'
    success_url = reverse_lazy("mailwork:recipient_list")


class RecipientDetailView(LoginRequiredMixin, DetailView):
    """ Контроллер для отображения экземпляра класса Recipient """
    model = Recipient


class RecipientUpdateView(LoginRequiredMixin, UpdateView):
    """ Контроллер для редактирования экземпляра класса Recipient """
    model = Recipient
    form_class = RecipientForm
    template_name = 'mailwork/recipient_form.html'
    success_url = reverse_lazy("mailwork:recipient_list")


class RecipientDeleteView(LoginRequiredMixin, DeleteView):
    """ Контроллер для удаления экземпляра класса Recipient """
    model = Recipient


class MessageListView(LoginRequiredMixin, ListView):
    """ Контроллер для отображения списка сообщений """
    model = Message
    context_object_name = "messages"
    template_name = "mailwork/messages_list.html"


class MessageCreateView(LoginRequiredMixin, CreateView):
    """ Контроллер для создания экземпляра класса Message """
    model = Message
    form_class = MessageForm
    template_name = 'mailwork/message_form.html'
    success_url = reverse_lazy("mailwork:messages_list")


class MessageDetailView(LoginRequiredMixin, DetailView):
    """ Контроллер для отображения экземпляра класса Message """
    model = Message


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    """ Контроллер для редактирования экземпляра класса Message """
    model = Message
    form_class = MessageForm
    template_name = 'mailwork/message_form.html'
    success_url = reverse_lazy("mailwork:messages_list")


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    """ Контроллер для удаления экземпляра класса Message """
    model = Message

@login_required
@permission_required('mailwork.can_unpublish_message', raise_exception=True)
def publish_message(request, message_id):
    message = get_object_or_404(Message, pk=message_id)
    message.is_published = True
    message.save()
    return redirect('catalog:non_published_products')


@login_required
@permission_required('mailwork.can_unpublish_message', raise_exception=True)
def unpublish_message(request, message_id):
    message = get_object_or_404(Message, pk=message_id)
    message.is_published = False
    message.save()
    return redirect('mailwork:non_published_messages')


class NewsLetterListView(LoginRequiredMixin, ListView):
    """ Контроллер для отображения списка рассылок """
    model = NewsLetter
    context_object_name = "newsletters"
    template_name = "mailwork/newsletters_list.html"


class NewsLetterCreateView(LoginRequiredMixin, CreateView):
    """ Контроллер для создания экземпляра класса NewsLetter """
    model = NewsLetter
    form_class = NewsLetterForm
    template_name = 'mailwork/newsletter_form.html'
    success_url = reverse_lazy("mailwork:newsletters_list")

    def form_valid(self, form):
        # Создаем объект рассылки, но не сохраняем в базе данных
        newsletter = form.save(commit=False)
        # Устанавливаем владельца рассылки (текущий пользователь)
        newsletter.owner = self.request.user

        # Сохраняем объект рассылки в базе данных
        newsletter.save()

        # Если форма уже содержит получателей, не забудьте их установить
        for recipient in form.cleaned_data.get('recipients', []):
            newsletter.recipients.add(recipient)

        return super().form_valid(form)


class NewsLetterDetailView(LoginRequiredMixin, DetailView):
    """ Контроллер для отображения экземпляра класса NewsLetter """
    model = NewsLetter


class NewsLetterUpdateView(LoginRequiredMixin, UpdateView):
    """ Контроллер для редактирования экземпляра класса NewsLetter """
    model = NewsLetter
    form_class = NewsLetterForm
    template_name = 'mailwork/newsletter_update.html'  # Исправьте путь к шаблону, если требуется
    success_url = reverse_lazy("mailwork:newsletters_list")

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()  # Получение текущего объекта
        # Логика для "запуска" или "завершения" рассылки.
        # Пример:
        if 'start' in request.POST:
            self.object.start()
        elif 'finish' in request.POST:
            self.object.finish()

        # Попытка сохранить объект и обработка ошибок
        try:
            self.object.save()
            return super().form_valid(self.get_form())
        except ValueError as e:
            print(f"Ошибка сохранения: {e}")  # Печать ошибки для отладки
            # Убедитесь, что форма будет невалидной и передаем ошибки
            return self.form_invalid(self.get_form())


class NewsLetterDeleteView(LoginRequiredMixin, DeleteView):
    """ Контроллер для удаления экземпляра класса NewsLetter """
    model = NewsLetter


class HomeTemplateView(TemplateView):
    """Выполняет переход к главной странице"""

    template_name = "mailwork/home.html"


class NonPublishedMessageListView(ListView):
    model = Message
    context_object_name = 'non_published_messages'
    template_name = 'mailwork/non_published_messages.html'

    def get_queryset(self):
        return Message.objects.filter(is_published=False)


class UserOwnedMessageListView(LoginRequiredMixin, ListView):
    model = Message
    context_object_name = 'owned_messages'
    template_name = 'mailwork/user_owner_messages.html'

    def get_queryset(self):
        return Message.objects.filter(owner=self.request.user)


class UserOwnerNewslettersListView(LoginRequiredMixin, ListView):
    model = NewsLetter
    context_object_name = 'owned_newsletters'
    template_name = 'mailwork/user_owner_newsletters.html'

    def get_queryset(self):
        return Message.objects.filter(owner=self.request.user)


class NonPublishedNewslettersListView(ListView):
    model = NewsLetter
    context_object_name = 'non_published_newsletters'
    template_name = 'mailwork/non_published_newsletters.html'

    def get_queryset(self):
        return Message.objects.filter(is_published=False)


class SendingAttemptCreateView(LoginRequiredMixin, CreateView):
    model = SendingAttempt
    context_object_name = 'newsletter_start'
    template_name = 'mailwork/newsletter_start.html'


# Обработчик для запуска рассылки
def newsletter_start(request, pk):
    newsletter = get_object_or_404(NewsLetter, pk=pk)

    if request.method == 'POST':
        print(f"Получен POST-запрос для рассылки с pk={pk}")
        try:
            if newsletter.status != 'started':
                newsletter.status = 'started'
                current_time = timezone.now()  # Используем правильный метод для получения текущего времени
                newsletter.first_send_time = current_time
                newsletter.last_send_time = current_time
                newsletter.save()

                sending_attempt = SendingAttempt(newsletter=newsletter)
                sending_attempt.attempt_time = current_time  # Устанавливаем текущее время для attempt_time

                try:
                    sending_attempt.send_newsletter(request.user)  # Попытка отправки
                    sending_attempt.status = 'success'  # Успех
                    messages.success(request, 'Рассылка успешно начата!')
                except Exception as e:  # Ловим исключения при отправке
                    sending_attempt.status = 'failure'  # Неудача
                    sending_attempt.server_response = str(e)  # Сохраняем сообщение об ошибке
                    messages.error(request, 'Ошибка при отправке рассылки!')

                sending_attempt.save()  # Сохраняем попытку в БД
                return redirect('mailwork:newsletters_list')
            else:
                messages.warning(request, 'Рассылка уже запущена!')
        except Exception as e:
            messages.error(request, f'Ошибка при запуске рассылки: {str(e)}')

    return redirect('mailwork:newsletters_list')

# Обработчик для завершения рассылки
def newsletter_finish(request, pk):
    newsletter = get_object_or_404(NewsLetter, pk=pk)

    if request.method == 'POST':  # Проверяем, что это POST-запрос
        try:
            newsletter.status = 'completed'  # Меняем статус на "Завершена"
            print(newsletter.__dict__)  # Выводим все поля объекта перед валидацией
            newsletter.full_clean()  # Проверяем валидацию данных перед сохранением
            newsletter.save()  # Сохраняем изменения
            messages.success(request, 'Рассылка успешно завершена!')  # Успешное сообщение
        except Exception as e:
            # Добавьте информацию об ошибках валидации
            errors = ''
            if hasattr(e, 'error_list'):  # Проверка наличия ошибок валидации
                # Обрабатываем ошибки валидации
                errors = ', '.join([str(error) for error in e.error_list])
            else:
                # Если ошибка не валидации, просто выводим ее
                errors = str(e)
            messages.error(request, f'Ошибка при завершении рассылки: {errors}')  # Сообщение об ошибке

    return redirect('mailwork:newsletters_list')  # Возврат на страницу списка рассылок


def footer_view(request):
    # Получаем статистику
    statistics = NewsLetter.overall_statistics()  # Получаем общую статистику

    return render(request, 'mailwork/includes/inc_footer.html', {'statistics': statistics})
