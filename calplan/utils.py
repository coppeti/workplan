import locale
import calendar
from datetime import date, timedelta
from django.db.models import Q


from accounts.models import User
from events.models import Event

locale.setlocale(locale.LC_ALL, 'fr_FR')


def a_year(which):
    if which == 'this':
        return date.today().year
    if which == 'prev':
        return date.today().year - 1
    if which == 'next':
        return date.today().year + 1


def date_between(start, end):
    start_date = date.fromisoformat(start)
    end_date = date.fromisoformat(end)
    delta = end_date - start_date
    return [(start_date + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(delta.days + 1)]


def planning(theuser, theyear, themonth):
    e = {}
    event = Event.objects.filter(Q(user_id=theuser), Q(date_start__year=theyear, date_start__month=themonth) |
                          Q(date_stop__year=theyear, date_stop__month=themonth))
    print(list(event))



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
        return f'<th class="{self.cssclass_month_head}">{s}</th>'

    def formatmonth(self, theyear, themonth, withyear=False):
        v = []
        a = v.append
        a(f'<tr class="{self.cssclass_month_head}">\n')
        a(f'{self.formatmonthname(theyear, themonth, withyear=withyear)}\n')
        for d, d_name in self.itermonthdays2(theyear, themonth):
            if d != 0:
                a(f'<td>{calendar.day_abbr[d_name]}</td>\n')
        a('</tr>\n')
        return ''.join(v)

    def formatuser(self, theyear, themonth):
        users = User.objects.order_by('last_name')
        for user in users:
            planning(user.pk, theyear, themonth)
        v = []
        a = v.append
        for user in users:
            a(f'<tr>\n')
            a(f'<td>{user.last_name.upper()}</td>\n')
            for d in self.itermonthdays2(theyear, themonth):
                if d != 0:
                    a(f'<td></td>\n')
            a(f'</tr>\n')
        return ''.join(v)

    def formatyear(self, theyear):
        v = []
        a = v.append
        for i in range(calendar.January, calendar.January+12):
            a(self.formatmonth(theyear, i))
            a(self.formatuser(theyear, i))
        a(self.formatmonth(theyear + 1, 1, withyear=True))
        a(self.formatuser(theyear, i))
        return ''.join(v)
