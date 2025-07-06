from django.contrib import admin

from mailwork.models import Message, NewsLetter, Recipient, SendingAttempt


@admin.register(Recipient)
class RecipientAdmin(admin.ModelAdmin):
    list_display = ("id", "email", "fullname", "comment")


@admin.register(Message)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "theme")
    search_fields = ("theme", "content")


@admin.register(NewsLetter)
class NewsLetterAdmin(admin.ModelAdmin):
    list_display = ["first_send_time", "last_send_time", "status", "message"]
