import holidays
from django.views.generic import TemplateView

from .utils import a_year, Calendar


class CalplanIndex(TemplateView):
    template_name = 'calplan/calplan-index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        year = a_year('this')
        context['cal'] = Calendar().formatyear(year)
        return context


class Holidays(TemplateView):
    template_name = 'calplan/holidays.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['year'] = kwargs['year']
        context['prev_year'] = context['year'] - 1
        context['next_year'] = context['year'] + 1
        context['after_year'] = a_year('next')
        context['region'] = kwargs['region']
        context['holidays'] = holidays.CH(subdiv=context['region'], years=context['year'])
        return context

