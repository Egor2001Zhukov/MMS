from django.contrib.auth.views import LogoutView, PasswordResetView
from django.urls import path

from users import views as v
from users.apps import UsersConfig

app_name = UsersConfig.name

urlpatterns = [
    path('profile/', v.UserUpdateView.as_view(), name='profile'),
    path('profile/change-avatar/', v.change_avatar, name='change_avatar'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('', v.UserLoginView.as_view(template_name='users/user_form.html'), name='login'),
    path('register/', v.RegisterView.as_view(), name='register'),
    path('verify_email/<str:token>/', v.VerifyEmailView.as_view(), name='verify_email'),
    path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
    path('confirm_password_reset/<str:token>/', v.ConfirmPasswordResetView.as_view(), name='confirm_reset_password'),
    path('change_active_user/<int:pk>/', v.change_active_user_view, name='change_active_user'),
]
