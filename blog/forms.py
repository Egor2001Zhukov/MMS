from django import forms

from blog import models as m


class BlogEntryForm(forms.ModelForm):
    class Meta:
        model = m.BlogEntry
        fields = ('title', 'content', 'img', 'is_publish',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, forms.BooleanField):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'
