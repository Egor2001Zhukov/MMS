import os
import random
import string

from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import Group
from django.contrib.auth.views import LoginView
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.http import JsonResponse, HttpResponse, HttpResponseForbidden
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views import generic as g

from config import settings
from mailing_management_service.models import Mailing
from users.forms import UserProfileForm, UserAuthenticationForm, RegisterForm
from users.models import User


class UserUpdateView(g.UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('user:profil')

    def get_object(self, queryset=None):
        return self.request.user


def change_avatar(request):
    if request.method == "POST" and request.FILES.get("avatar"):
        user = request.user
        try:
            old_avatar = os.path.join(settings.MEDIA_ROOT, f'{user.avatar}')
            os.remove(old_avatar)
        finally:
            user.avatar = request.FILES["avatar"]
            user.save()
            return JsonResponse({"message": "Аватар успешно обновлен!"})
    return JsonResponse({"error": "Произошла ошибка при обновлении аватара."}, status=400)


class UserLoginView(LoginView):
    form_class = UserAuthenticationForm

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(to=reverse_lazy('user:profile'))
        else:
            return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        user = User.objects.get(email=form.cleaned_data.get('username'))
        if user.email_verified:
            return super().form_valid(form)
        else:
            form.add_error('username', 'Нужно подтвердить почту')
            return self.form_invalid(form)


class RegisterView(g.CreateView):
    model = User
    form_class = RegisterForm
    success_url = reverse_lazy('user:login')

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(to=reverse_lazy('user:profile'))
        else:
            return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)
        new_user = form.save()
        if not new_user.avatar:
            new_user.avatar = 'users/user.png'
        # Создаем и сохраняем токен подтверждения
        token = ''.join(random.choices(string.ascii_letters + string.digits, k=50))
        new_user.email_verification_token = token
        new_user.save()
        # Отправляем письмо с подтверждением
        current_site = get_current_site(self.request)
        mail_subject = ('Подтвердите ваш аккаунт. '
                        'Пройдите по этой ссылке для подтверждения регистрации:')
        message = render_to_string(
            'users/email_verified.html',
            {
                'domain': current_site.domain,
                'token': token,
            },
        )
        send_mail(mail_subject, message, os.getenv('EMAIL_HOST_USER'), [new_user.email])
        return response


class VerifyEmailView(g.View):
    def get(self, request, token):
        try:
            user = User.objects.get(email_verification_token=token)
            user.email_verified = True
            user.save()
            return redirect('user:login')  # Редирект на страницу входа
        except User.DoesNotExist:
            return HttpResponse('Неверная ссылка подтверждения.')


class ConfirmPasswordResetView(g.View):
    def get(self, request, token):
        user = User.objects.get(email_verification_token=token)
        new_password = ''.join([str(random.randint(0, 9)) for _ in range(12)])
        user.set_password(new_password)
        user.save()
        return render(request, 'users/confirm_password_reset.html',
                      {'new_password': new_password})


class ModeratorInterfaceView(g.View):
    def get(self, request):
        moderators = Group.objects.get(name="moderators").user_set.all()
        if self.request.user not in moderators:
            return HttpResponseForbidden("Доступ запрещен")
        users = User.objects.all().order_by('-date_joined')
        mailings = Mailing.objects.all().order_by('-created_at')
        context = {
            'users': users,
            'mailings': mailings
        }
        return render(request, 'users/moderator_interface.html', context=context)


@permission_required('user.deactivate_user')
def change_active_user_view(request, pk):
    user = User.objects.get(pk=pk)
    if user.is_active:
        user.is_active = False
    else:
        user.is_active = True
    user.save()
    return redirect(reverse_lazy('moderator_interface'))
