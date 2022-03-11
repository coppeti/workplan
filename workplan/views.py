import holidays
from django.views.generic import ListView, CreateView, UpdateView, TemplateView

from config.utils import a_year
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


class Holidays(TemplateView):
    template_name = 'workplan/holidays.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['year'] = kwargs['year']
        context['current_year'] = a_year('this')
        context['next_year'] = a_year('next')
        context['region'] = kwargs['region']
        context['holidays'] = holidays.CH(subdiv=context['region'], years=context['year'])
        return context

