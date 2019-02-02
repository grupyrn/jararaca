from itertools import groupby
from operator import attrgetter

from django.utils import formats


def date_range_format(dates: list):
    text = ''

    total = len(list(groupby(dates, key=attrgetter('month'))))

    i = -1
    for month, dates_month in groupby(dates, key=attrgetter('month')):
        dates_month = list(dates_month)
        i += 1
        for date in dates_month:
            # middle
            if not date == dates_month[0] and not date == dates_month[-1]:
                text += formats.date_format(date, ', d', True)
            # first
            elif date == dates_month[0] and not date == dates_month[-1]:
                text += formats.date_format(date, 'd', True)
            # last
            elif date == dates_month[-1] and not date == dates_month[0]:
                text += formats.date_format(date, ' \e d \d\e F \d\e Y', True)
            # only
            elif date == dates_month[0] and date == dates_month[0]:
                text += formats.date_format(date, 'd \d\e F \d\e Y', True)
        if i == total - 2:
            text += ' e '
        elif total == 1:
            pass
        elif i < total - 2:
            text += ', '

    return text


def scale_to_width(dimensions, width):
    height = (width * dimensions[1]) / dimensions[0]
    return int(width), int(height)
