from django.contrib.auth.decorators import login_required
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from users.apps import UsersConfig
from .views import RegisterView, email_verification, CustomLoginView, EditProfileView, ProfileSuccessView

app_name = UsersConfig.name

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(template_name='users/login.html', success_url='/mailwork/messages_list/'), name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('email-confirm/<str:token>/', email_verification, name='email-confirm'),
    path('edit_profile/', EditProfileView.as_view(), name='edit_profile'),
    path('profile/success/', login_required(ProfileSuccessView.as_view()), name='profile_success'),

]
