from django import forms
from django.core.exceptions import ValidationError
from django.db.models import Q

from .models import Event, Activity
from accounts.models import User


class CreateEventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['user_id', 'activity_id', 'date_start', 'date_stop', 'confirmed']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        # if self.user.groups.filter(name__iexact='Administrator').exists():
        #     self.fields['user_id'].queryset = User.objects.all()
        #     self.fields['activity_id'].queryset = Activity.objects.all()
        #     self.fields['confirmed'] = forms.BooleanField()
        # else:
        if self.user.groups.filter(name__iexact='User').exists():
            self.fields['user_id'].initial = self.user
            self.fields['user_id'].queryset = User.objects.filter(id=self.user.pk)
            self.fields['activity_id'].queryset = Activity.objects.exclude(Q(name='dispatcher') |
                                                                           Q(name='pikett'))
            self.fields['confirmed'].widget = forms.HiddenInput()
            self.fields['confirmed'].initial = False

    def clean(self):
        cleaned_data = super().clean()
        user = cleaned_data.get('user_id')
        activity = cleaned_data.get('activity_id')
        date_start = cleaned_data.get('date_start')
        date_stop = cleaned_data.get('date_stop')
        confirmed = cleaned_data.get('confirmed')

        # Control of activities in conflict with demand
        event = Event.objects.filter(Q(user_id=user), Q(confirmed=True),
                                     Q(date_start__lte=date_stop, date_stop__gte=date_start) |
                                     Q(date_stop__gte=date_start, date_stop__lte=date_stop))
        if event:
            for e in event:
                if (confirmed and activity != 'kein pikett' and e.activity_id.name != 'kein pikett') \
                        or (confirmed and activity == 'pikett' and e.activity_id.name == 'kein pikett') or \
                        (confirmed and activity == 'kein pikett' and e.activity_id.name == 'pikett'):
                    raise ValidationError(f"{e.user_id} has already"
                                          f"{e.activity_id.name.title()}: {e.date_start} - {e.date_stop}")


class EditEventForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        logged_user = kwargs.pop('user')
        event = kwargs.get('instance')
        super(EditEventForm, self).__init__(*args, **kwargs)
        print(self.instance.activity_id)
        if logged_user.groups.filter(name__iexact='User').exists():
            if event.activity_id.name == 'pikett' or event.activity_id.name == 'dispatcher':
                self.fields['activity_id'].queryset = Activity.objects.filter(name=event.activity_id.name)
                self.fields['confirmed'].widget = forms.HiddenInput()
            if event.activity_id.name != 'pikett' and event.activity_id.name != 'dispatcher':
                self.fields['user_id'].queryset = User.objects.filter(pk=logged_user.pk)
                self.fields['activity_id'].queryset = Activity.objects.exclude(Q(name='dispatcher') |
                                                                               Q(name='pikett'))
                self.fields['confirmed'].widget = forms.HiddenInput()

    class Meta:
        model = Event
        fields = ['user_id', 'activity_id', 'date_start', 'date_stop', 'confirmed']



    def clean(self):
        cleaned_data = super().clean()
        user = cleaned_data.get('user_id')
        activity = cleaned_data.get('activity_id')
        date_start = cleaned_data.get('date_start')
        date_stop = cleaned_data.get('date_stop')
        confirmed = cleaned_data.get('confirmed')

        # Control of activities in conflict with demand
        event = Event.objects.filter(Q(user_id=user), Q(confirmed=True),
                                     Q(date_start__lte=date_stop, date_stop__gte=date_start) |
                                     Q(date_stop__gte=date_start, date_stop__lte=date_stop))
        if event:
            for e in event:
                if confirmed:
                    raise ValidationError(f"{e.user_id} has already {e.activity_id.name.title()}:"
                                          f" {e.date_start} - {e.date_stop}")

