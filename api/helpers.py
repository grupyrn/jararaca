from itertools import groupby
from operator import attrgetter


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
                text += date.strftime(', %d')
            # first
            elif date == dates_month[0] and not date == dates_month[-1]:
                text += date.strftime('%d')
            # last
            elif date == dates_month[-1] and not date == dates_month[0]:
                text += date.strftime(' e %d de %B de %Y')
            # only
            elif date == dates_month[0] and date == dates_month[0]:
                text += date.strftime('%d de %B de %Y')
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
