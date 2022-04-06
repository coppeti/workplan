from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.views.generic import CreateView, UpdateView, ListView

from calplan.utils import a_year
from .forms import CreateEventForm
from .models import Event


class EventIndex(LoginRequiredMixin, ListView):
    model = Event
    queryset = Event.objects.filter(Q(date_start__year=a_year('this')) | Q(date_stop__year=a_year('this')))
    ordering = 'user_id__last_name', 'date_start'


class NewEvent(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = 'events/event_form.html'
    form_class = CreateEventForm
    success_url = '/event'
    success_message = 'Your request has been registered and will soon be validated.'

    def get_form_kwargs(self):
        kwargs = super(NewEvent, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class EditEvent(LoginRequiredMixin, UpdateView):
    model = Event
    fields = ['user_id', 'activity_id', 'date_start', 'date_stop']
    success_url = '/event'
