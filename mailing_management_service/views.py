from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import generic as g

from mailing_management_service import forms as f
from mailing_management_service import models as m
from mailing_management_service import services
from users.models import User


class MailingListView(LoginRequiredMixin, g.ListView):
    model = m.Mailing
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = super().get_queryset().filter(user=self.request.user)
        return queryset


class MailingCreateView(LoginRequiredMixin, g.CreateView):
    model = m.Mailing
    success_url = reverse_lazy('mms:mailing_list')
    form_class = f.MailingForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        mailing = form.save(commit=False)
        mailing.user = self.request.user
        mailing.save()
        return super().form_valid(form=form)


class MailingUpdateView(LoginRequiredMixin, g.UpdateView):
    model = m.Mailing
    form_class = f.MailingForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        kwargs['instance'] = self.object
        return kwargs

    def get(self, request, *args, **kwargs):
        if services.is_creator(self.request.user, m.Mailing.objects.get(pk=kwargs.get('pk'))):
            return super().get(request)
        return HttpResponseForbidden("Доступ запрещен")

    def form_valid(self, form):
        if services.is_creator(self.request.user, self.object):
            response = super().form_valid(form)
            services.update_cron_task_mailing(self.object)
            return response
        return HttpResponseForbidden("Доступ запрещен")

    def get_success_url(self):
        return reverse_lazy('mms:view_mailing', kwargs={'pk': self.object.pk})


class MailingDetailView(LoginRequiredMixin, g.DetailView):
    model = m.Mailing


class MailingDeleteView(LoginRequiredMixin, g.DeleteView):
    model = m.Mailing
    success_url = reverse_lazy('mms:mailing_list')

    def get(self, request, *args, **kwargs):
        if services.is_creator(self.request.user, m.Mailing.objects.get(pk=kwargs.get('pk'))):
            return super().get(request)
        return HttpResponseForbidden("Доступ запрещен")

    def form_valid(self, form):
        if services.is_creator(self.request.user, self.object):
            return super().form_valid(form)
        return HttpResponseForbidden("Доступ запрещен")


def change_letter_view(request, pk):
    letter_pk = request.POST.get('letter')
    if letter_pk:
        letter = m.Letter.objects.get(pk=letter_pk)
    else:
        letter = None
    mailing = m.Mailing.objects.get(pk=pk)
    mailing.letter = letter
    mailing.save()
    return redirect(to=reverse_lazy('mms:mailing_list'))


def change_is_launched_view(request, pk):
    mailing = m.Mailing.objects.get(pk=pk)
    if services.is_moderator_or_creator(request.user, mailing):
        if mailing.is_launched:
            mailing.is_launched = False
            services.remove_cron_task_mailing(mailing)
        else:
            mailing.is_launched = True
            services.add_cron_task_mailing(mailing)
        mailing.save()
        return redirect(to=request.META.get('HTTP_REFERER', reverse_lazy('mms:mailing_list')))
    else:
        return HttpResponseForbidden("Доступ запрещен")


class LetterCreateView(LoginRequiredMixin, g.CreateView):
    model = m.Letter
    success_url = reverse_lazy('mms:letter_list')
    form_class = f.LetterForm

    def form_valid(self, form):
        letter = form.save(commit=False)
        letter.user = self.request.user
        letter.save()
        return super().form_valid(form=form)


class LetterListView(LoginRequiredMixin, g.ListView):
    model = m.Letter

    def get_queryset(self):
        queryset = super().get_queryset().filter(user=self.request.user)
        return queryset


class LetterDetailView(LoginRequiredMixin, g.DetailView):
    model = m.Letter


class LetterUpdateView(LoginRequiredMixin, g.UpdateView):
    model = m.Letter
    form_class = f.LetterForm

    def get(self, request, *args, **kwargs):
        if services.is_creator(self.request.user, m.Letter.objects.get(pk=kwargs.get('pk'))):
            return super().get(request)
        return HttpResponseForbidden("Доступ запрещен")

    def get_success_url(self):
        return reverse_lazy('mms:view_letter', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        if services.is_creator(self.request.user, self.object):
            return super().form_valid(form)
        return HttpResponseForbidden("Доступ запрещен")


class LetterDeleteView(LoginRequiredMixin, g.DeleteView):
    model = m.Letter
    success_url = reverse_lazy('mms:letter_list')

    def get(self, request, *args, **kwargs):
        if services.is_creator(self.request.user, m.Letter.objects.get(pk=kwargs.get('pk'))):
            return super().get(request)
        return HttpResponseForbidden("Доступ запрещен")

    def form_valid(self, form):
        if services.is_creator(self.request.user, self.object):
            return super().form_valid(form)
        return HttpResponseForbidden("Доступ запрещен")


class MailingLogListView(g.ListView):
    model = m.MailingLog
    ordering = ['-last_time']

    def get_queryset(self):
        return super().get_queryset().filter(mailing=m.Mailing.objects.get(pk=self.kwargs.get('pk')))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['mailing'] = m.Mailing.objects.get(pk=self.kwargs.get('pk'))
        return context


class HomeView(g.View):
    def get(self, request):
        context = {
            'mailing': len(m.Mailing.objects.all()),
            'mailing_active': len(m.Mailing.objects.filter(is_launched=True)),
            'users': len(User.objects.filter(is_active=True)),
        }
        return render(request, template_name='main.html', context=context)


class RecipientCreateView(LoginRequiredMixin, g.CreateView):
    model = m.Recipient
    success_url = reverse_lazy('mms:recipient_list')
    form_class = f.RecipientForm

    def form_valid(self, form):
        letter = form.save(commit=False)
        letter.user = self.request.user
        letter.save()
        return super().form_valid(form=form)


class RecipientListView(LoginRequiredMixin, g.ListView):
    model = m.Recipient

    def get_queryset(self):
        queryset = super().get_queryset().filter(user=self.request.user)
        return queryset


class RecipientDetailView(LoginRequiredMixin, g.DetailView):
    model = m.Recipient


class RecipientUpdateView(LoginRequiredMixin, g.UpdateView):
    model = m.Recipient
    form_class = f.RecipientForm

    def get(self, request, *args, **kwargs):
        if services.is_creator(self.request.user, m.Recipient.objects.get(pk=kwargs.get('pk'))):
            return super().get(request)
        return HttpResponseForbidden("Доступ запрещен")

    def get_success_url(self):
        return reverse_lazy('mms:view_recipient', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        if services.is_creator(self.request.user, self.object):
            return super().form_valid(form)
        return HttpResponseForbidden("Доступ запрещен")


class RecipientDeleteView(LoginRequiredMixin, g.DeleteView):
    model = m.Recipient
    success_url = reverse_lazy('mms:recipient_list')

    def get(self, request, *args, **kwargs):
        if services.is_creator(self.request.user, m.Recipient.objects.get(pk=kwargs.get('pk'))):
            return super().get(request)
        return HttpResponseForbidden("Доступ запрещен")

    def form_valid(self, form):
        if services.is_creator(self.request.user, self.object):
            return super().form_valid(form)
        return HttpResponseForbidden("Доступ запрещен")
