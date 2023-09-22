from django import forms

from mailing_management_service import models as m


class MailingForm(forms.ModelForm):
    class Meta:
        model = m.Mailing
        fields = '__all__'
        exclude = ('is_launched', 'user',)

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, forms.BooleanField):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'
        letter_choices = m.Letter.objects.filter(user=user).values_list('pk', 'subject')
        self.fields['letter'].widget.choices = letter_choices


class LetterForm(forms.ModelForm):
    class Meta:
        model = m.Letter
        fields = '__all__'
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, forms.BooleanField):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'


class LetterChoiceForm(forms.ModelForm):
    class Meta:
        model = m.Mailing
        fields = ('letter',)

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, forms.BooleanField):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'
        letter_choices = m.Letter.objects.filter(user=user).values_list('pk', 'subject')
        self.fields['letter'].widget.choices = letter_choices


class RecipientForm(forms.ModelForm):
    class Meta:
        model = m.Recipient
        fields = '__all__'
        exclude = ('user', 'is_active')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, forms.BooleanField):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'
