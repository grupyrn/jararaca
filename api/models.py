import json

from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.utils.text import format_lazy
from django.utils.translation import gettext_lazy as _
import uuid
from datetime import date, datetime


class MemberInfo(object):
    def __init__(self, name, email, cpf=None):
        self.name = name
        self.email = email
        self.cpf = cpf

    def to_json(self):
        func = lambda o: {k: v for k, v in o.__dict__.items()
                          if v is not None}

        return json.dumps(self, default=func,
                          sort_keys=True)


class Attendee(models.Model):
    uuid = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    event = models.ForeignKey('Event', verbose_name=_('event'), on_delete=models.CASCADE)
    name = models.CharField(_('name'), max_length=500)
    email = models.EmailField(_('email'), max_length=50)
    cpf = models.CharField(_('CPF'), max_length=11)
    share_data_with_partners = models.BooleanField(_('share data with partners'), default=False)
    date = models.DateTimeField(_('date'), auto_now_add=True)

    class Meta:
        verbose_name = _('attendee')
        verbose_name_plural = _('attendees')


class Event(models.Model):
    name = models.CharField(_('name'), max_length=500)
    description = models.TextField(_('description'), blank=True)
    place = models.CharField(_('place'), max_length=500)
    latitude = models.FloatField(_('latitude'))
    longitude = models.FloatField(_('longitude'))
    organizers = models.CharField(_('organizers'), max_length=500)
    created_by = models.ForeignKey(get_user_model(), _('created by'), null=True)
    slug = models.SlugField(unique=True)
    content_link = models.URLField(_('content link'), null=True)

    @property
    def date(self):
        return self.eventday_set.order_by('date').values_list('date', flat=True).all()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('event')
        verbose_name_plural = _('events')


class EventDay(models.Model):
    event = models.ForeignKey('Event', verbose_name=_('event'), on_delete=models.CASCADE)
    date = models.DateField(_('date'))
    start = models.TimeField(_('start time'))
    end = models.TimeField(_('end time'))

    @mark_safe
    def schedule_link(self):
        print('id: ', self.id)
        if self.id:
            changeform_url = reverse(
                'admin:api_eventday_change', args=(self.id,)
            )
            return '<a href="%s" target="_blank">%s</a>' % (changeform_url, _('change schedule').title())
        return u''

    schedule_link.short_description = ''

    def __str__(self):
        return f'{self.event.name} - {self.date}'

    class Meta:
        verbose_name = _('event day')
        verbose_name_plural = _('event days')


class EventSchedule(models.Model):
    event = models.ForeignKey('EventDay', verbose_name=_('event day'), on_delete=models.CASCADE)
    start = models.TimeField(_('start time'))
    end = models.TimeField(_('end time'))
    title = models.CharField(_('title'), max_length=150)
    place = models.CharField(_('place'), max_length=150, blank=True)
    description = models.TextField(_('description'), blank=True)
    authors = models.CharField(_('authors'), max_length=500, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('event schedule')
        verbose_name_plural = _('event schedules')


class EventDayCheck(models.Model):
    attendee = models.ForeignKey('Attendee', verbose_name=_('attendee'), on_delete=models.CASCADE)
    event_day = models.ForeignKey('EventDay', verbose_name=_('event day'), on_delete=models.CASCADE)
    entrance_date = models.DateTimeField(_('entrance date/time'), auto_now_add=True)
    exit_date = models.DateTimeField(_('exit date/time'), null=True)

    @property
    def time_passed(self):
        return self.exit_date - self.entrance_date if self.exit_date else None

    def attendee_name(self):
        return self.attendee.name

    def event(self):
        return self.event_day.event

    time_passed.fget.short_description = _('permanence time')

    def __str__(self):
        text = _('permanence time')
        passed = format_lazy('{text}: {time}', text=text, time=self.time_passed)
        if not self.time_passed:
            passed = _('not checked out')
        return f'{self.attendee.name} - {passed}'

    def checkout(self):
        if not self.exit_date:
            self.exit_date = timezone.now()
            self.save()

        delta_event = datetime.combine(date.min, self.event_day.end) - datetime.combine(date.min, self.event_day.start)
        delta_check = self.exit_date - self.entrance_date
        result = delta_check.seconds * 100 / delta_event.seconds

        return result >= 75

    class Meta:
        verbose_name = _('event day check')
        verbose_name_plural = _('event day checks')
