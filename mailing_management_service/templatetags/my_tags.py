from django import template
from django.contrib.auth.models import Group

from mailing_management_service import models as m
from mailing_management_service.forms import LetterChoiceForm

register = template.Library()


@register.simple_tag()
def get_letter_form(mailing_pk, user):
    mailing = m.Mailing.objects.get(pk=mailing_pk)
    if mailing:
        if mailing.letter:
            form = LetterChoiceForm(user=user, initial={'letter': mailing.letter}, )
            # letter_choices = m.Letter.objects.filter(user=user).values_list('pk', 'subject')
            # form.fields['letter'].widget.choices = letter_choices
            return form
    return LetterChoiceForm(user=user, )


# Создание фильтра
@register.filter()
def mediapath(val):
    if val:
        return f'/media/{val}'
    return ''


@register.filter()
def is_moderator(val):
    moderators = Group.objects.get(name="moderators").user_set.all()
    if val in moderators:
        return True
    return False
