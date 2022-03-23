from django.shortcuts import render
from django.views.generic import CreateView, UpdateView, ListView

from .models import Event


class EventIndex(ListView):
    model = Event


class NewEvent(CreateView):
    model = Event
    fields = ['user_id', 'activity_id', 'date_start', 'date_stop']
    success_url = '/event'


class EditEvent(UpdateView):
    model = Event
    fields = ['user_id', 'activity_id', 'date_start', 'date_stop']
    success_url = '/event'
