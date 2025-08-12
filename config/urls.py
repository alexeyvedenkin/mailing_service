from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("mailwork.urls", namespace="mailwork")),
    path("users/", include("users.urls", namespace="users")),
]
