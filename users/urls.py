from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView
from django.urls import path

from users.apps import UsersConfig

from .views import CustomLoginView, EditProfileView, ProfileSuccessView, RegisterView, email_verification, user_list, \
    block_user

app_name = UsersConfig.name

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path(
        "login/",
        CustomLoginView.as_view(template_name="users/login.html", success_url="/mailwork/messages_list/"),
        name="login",
    ),
    path("logout/", LogoutView.as_view(next_page="/"), name="logout"),
    path("email-confirm/<str:token>/", email_verification, name="email-confirm"),
    path("edit_profile/", EditProfileView.as_view(), name="edit_profile"),
    path("profile/success/", login_required(ProfileSuccessView.as_view()), name="profile_success"),

    path('users/', user_list, name='user_list'),
    path('users/block/<int:user_id>/', block_user, name='block_user'),
]
