import locale
import calendar
import holidays
from datetime import date, timedelta
from django.db.models import Q

from accounts.models import User
from events.models import Event

locale.setlocale(locale.LC_ALL, 'en_GB')

be_holidays = holidays.CH(subdiv='BE', years=date.today().year)


def a_year(which):
    if which == 'this':
        return date.today().year
    if which == 'prev':
        return date.today().year - 1
    if which == 'next':
        return date.today().year + 1


def date_between(start, end):
    start_date = date.fromisoformat(str(start))
    end_date = date.fromisoformat(str(end))
    delta = end_date - start_date
    dates = ((start_date + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(delta.days + 1))
    return tuple(dates)


def user_month_act(theuser, theyear, themonth):
    u_act = {}
    events = Event.objects.filter(Q(user_id=theuser), Q(confirmed=True), Q(is_active=True),
                                  Q(date_start__year=theyear, date_start__month=themonth) |
                                  Q(date_stop__year=theyear, date_stop__month=themonth))
    for e in events:
        dates = date_between(e.date_start, e.date_stop)
        u_act[dates] = e.activity_id.short_name
    return u_act


def user_line(cal, theuser, theyear, themonth):
    v = []
    a = v.append
    user_plan = user_month_act(theuser, theyear, themonth)
    for month_date in cal.itermonthdates(theyear, themonth):
        if month_date.month == themonth:
            a(f'<td>')
            for d, act in user_plan.items():
                if month_date.strftime("%Y-%m-%d") in d:
                    if act == 'F' and (month_date.weekday() == 5 or month_date.weekday() == 6 or
                                       month_date in be_holidays):
                        a('')
                    elif act == 'P' and month_date.weekday() == 5:
                        a('PSA')
                    elif (act == 'P' and month_date.weekday() == 6) or (act == 'P' and month_date in be_holidays):
                        a('PSO')
                    else:
                        a(act)
            a('</td>\n')
    return ''.join(v)


def holiday_line(cal, theyear, themonth):
    v = []
    a = v.append
    all_holiday = sum([holidays.CH(subdiv=x, years=theyear) for x in holidays.CH.subdivisions if x == 'BE' or x == 'AR'
                       or x == 'SO' or x == 'NE' or x == 'FR' or x == 'VD' or x == 'GE'])
    a('<tr>\n')
    for d in cal.itermonthdates(theyear, themonth):
        if d.month == themonth:
            a('<td>')
            if d in all_holiday:
                a(f'{all_holiday.get(d)}')
            a('</td>')
    a('</tr>')
    return ''.join(v)


class Calendar(calendar.HTMLCalendar):
    def __init__(self, year=None, month=None):
        self.year = year
        self.month = month
        super(Calendar, self).__init__()

    def formatmonthname(self, theyear, themonth, withyear=True):
        if withyear:
            s = f'{calendar.month_name[themonth]} {theyear}'
        else:
            s = f'{calendar.month_name[themonth]}'
        return f'<th rowspan="2" class="{self.cssclass_month_head}">{s}</th>'

    def formatmonth(self, theyear, themonth, withyear=False):
        v = []
        a = v.append
        a(f'<tr class="{self.cssclass_month_head}">\n')
        a(f'{self.formatmonthname(theyear, themonth, withyear=withyear)}\n')
        for d, d_name in self.itermonthdays2(theyear, themonth):
            if d != 0:
                a(f'<td>{calendar.day_abbr[d_name]}')
                if date(theyear, themonth, d).isocalendar()[2] == 1 or d == 1:
                    a(f'<span>{date(theyear, themonth, d).isocalendar()[1]}</span>')
                a('</td>\n')
        a('</tr>\n')
        a(holiday_line(self, theyear, themonth))
        return ''.join(v)

    def formatuser(self, theyear, themonth):
        v = []
        a = v.append
        users = User.objects.order_by('last_name')
        for user in users:
            a(f'<tr>\n')
            a(f'<td>{user.last_name.upper()}</td>\n')
            a(user_line(self, user.pk, theyear, themonth))
            a(f'</tr>\n')
        return ''.join(v)

    def formatyear(self, theyear):
        v = []
        a = v.append
        for i in range(calendar.January, calendar.January + 12):
            a(self.formatmonth(theyear, i))
            a(self.formatuser(theyear, i))
        a(self.formatmonth(theyear + 1, 1, withyear=True))
        a(self.formatuser(theyear, i))
        return ''.join(v)
