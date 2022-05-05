from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView, DeleteView

from calplan.utils import a_year
from .forms import CreateEventForm, EditEventForm
from .models import Event


class EventIndex(LoginRequiredMixin, ListView):
    model = Event
    queryset = Event.objects.filter(Q(date_start__year=a_year('this')) | Q(date_stop__year=a_year('this')))
    ordering = 'user_id__last_name', 'date_start'


class NewEvent(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = 'events/event_form.html'
    form_class = CreateEventForm
    success_url = '/event'
    # success_message = 'Your request has been registered and will soon be validated.'

    def get_form_kwargs(self):
        kwargs = super(NewEvent, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def form_valid(self, form):
        if self.request.user.groups == "Administrator":
            messages.success(self.request, "Your request has been registered.")
        else:
            messages.success(self.request, "Your request has been registered and will soon be validated.")
        super().form_valid(form)
        return HttpResponseRedirect(self.get_success_url())


class EditEvent(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Event
    template_name = 'events/event_form.html'
    form_class = EditEventForm
    success_url = '/event'
    success_message = 'Event has been updated.'

    def get_form_kwargs(self):
        kwargs = super(EditEvent, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def form_valid(self, form):
        return super().form_valid(form)


class DelEvent(DeleteView):
    model = Event
    success_url = reverse_lazy('event_index')