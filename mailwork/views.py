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
from mailwork.models import Message, NewsLetter, Recipient


class RecipientListView(LoginRequiredMixin, ListView):
    """ Контроллер для отображения списка получателей """
    model = Recipient
    context_object_name = "recipients"
    template_name = "recipients_list.html"

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
    template_name = "messages_list.html"

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

class NewsLetterListView(LoginRequiredMixin, ListView):
    """ Контроллер для отображения списка рассылок """
    model = NewsLetter
    context_object_name = "newsletters"
    template_name = "newsletters_list.html"

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

class NewsLetterDeleteView(LoginRequiredMixin, DeleteView):
    """ Контроллер для удаления экземпляра класса NewsLetter """
    model = NewsLetter
