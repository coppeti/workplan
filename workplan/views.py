from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView

from .models import Planning


class WorkplanIndex(ListView):
    model = Planning


class NewActivity(CreateView):
    model = Planning
    fields = ['user_id', 'activity_id', 'date_start', 'date_stop']
    success_url = '/workplan'


class EditActivity(UpdateView):
    model = Planning
    fields = ['user_id', 'activity_id', 'date_start', 'date_stop']
    success_url = '/workplan'
