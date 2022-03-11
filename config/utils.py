from datetime import date


def a_year(which):
    if which == 'this':
        return date.today().year
    elif which == 'next':
        return date.today().year + 1
