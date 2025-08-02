from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
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


class NewsLetterDetailView(LoginRequiredMixin, DetailView):
    """ Контроллер для отображения экземпляра класса NewsLetter """
    model = NewsLetter


class NewsLetterUpdateView(LoginRequiredMixin, UpdateView):
    """ Контроллер для редактирования экземпляра класса NewsLetter """
    model = NewsLetter
    form_class = NewsLetterForm
    template_name = 'mailwork/newsletters_form.html'
    success_url = reverse_lazy("mailwork:newsletters_list")

    # def newsletter_start(self):


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


# class NewsLetterStart(LoginRequiredMixin):
#     model = NewsLetter
#     context_object_name = 'newsletter_start'
#     template_name = 'mailwork/newsletter_start.html'
#
#
# class NewsLetterFinish(LoginRequiredMixin):
#     model = NewsLetter
#     context_object_name = 'newsletter_finish'
#     template_name = 'mailwork/newsletter_finish.html'
