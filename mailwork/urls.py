from django.urls import path

from mailwork.apps import MailworkConfig
from mailwork.views import (HomeTemplateView, MessageCreateView, MessageDeleteView, MessageDetailView, MessageListView,
                            MessageUpdateView, NewsLetterCreateView, NewsLetterDeleteView, NewsLetterDetailView,
                            NewsLetterListView, NewsLetterUpdateView, NonPublishedMessageListView,
                            NonPublishedNewslettersListView, RecipientCreateView, RecipientDeleteView,
                            RecipientDetailView, RecipientListView, RecipientUpdateView, UserOwnedMessageListView,
                            UserOwnerNewslettersListView, newsletter_finish, newsletter_start, publish_message,
                            unpublish_message)

app_name = MailworkConfig.name

urlpatterns = [
    # Главная страница
    path("", HomeTemplateView.as_view(), name="home"),

    # Адресаты
    path("recipients_list/", RecipientListView.as_view(), name="recipients_list"),
    path("recipient_detail/<int:pk>/", RecipientDetailView.as_view(), name="recipient_detail"),
    path("recipient_create/", RecipientCreateView.as_view(), name="recipient_create"),
    path("recipient/<int:pk>/update/", RecipientUpdateView.as_view(), name="recipient_update"),
    path("recipient/<int:pk>/delete/", RecipientDeleteView.as_view(), name="recipient_delete"),

    # Сообщения
    path("non_published_messages/", NonPublishedMessageListView.as_view(), name="non_published_messages"),
    path("owned-messages/", UserOwnedMessageListView.as_view(), name="user_owned_messages"),
    path("message/<int:message_id>/publish/", publish_message, name="publish_message"),
    path("message/<int:message_id>/unpublish/", unpublish_message, name="unpublish_message"),
    path("messages/", MessageListView.as_view(), name="messages_list"),
    path("message_create/", MessageCreateView.as_view(), name="message_create"),
    path("message/<int:pk>/", MessageDetailView.as_view(), name="message_detail"),
    path("message/<int:pk>/update/", MessageUpdateView.as_view(), name="message_update"),
    path("message/<int:pk>/delete/", MessageDeleteView.as_view(), name="message_delete"),

    # Рассылки
    path("newsletters/", NewsLetterListView.as_view(), name="newsletters_list"),
    path("newsletter_create/", NewsLetterCreateView.as_view(), name="newsletter_create"),
    path("newsletter/<int:pk>/", NewsLetterDetailView.as_view(), name="newsletter_detail"),
    path("newsletter/<int:pk>/update/", NewsLetterUpdateView.as_view(), name="newsletter_update"),
    path("newsletter/<int:pk>/delete/", NewsLetterDeleteView.as_view(), name="newsletter_delete"),
    path("newsletter/start/<int:pk>/", newsletter_start, name="newsletter_start"),  # Замените на функцию
    path("newsletter/finish/<int:pk>/", newsletter_finish, name="newsletter_finish"),
    path("user_owner_newsletters/", UserOwnerNewslettersListView.as_view(), name="user_owner_newsletters"),
    path("non_published_newsletters/", NonPublishedNewslettersListView.as_view(), name="non_published_newsletters"),
]
