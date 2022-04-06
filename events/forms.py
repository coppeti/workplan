from django import forms
from django.http import request

from .models import Event

LIST_CHOICES = (
    ('1', 'un'),
    ('2', 'deux'),
    ('3', 'trois'),
)

LIMITED_LIST_CHOICES = (
    ('bla', 'bla'),
    ('bli', 'bli'),
)


class CreateEventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['user_id', 'activity_id', 'date_start', 'date_stop']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        if self.user.groups.filter(name__iexact='Administrator').exists():
            self.fields['user_id'] = forms.ChoiceField(choices=LIST_CHOICES)
        else:
            self.fields['user_id'] = forms.ChoiceField(choices=LIMITED_LIST_CHOICES)





