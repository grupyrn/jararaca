import json

from django.db import models
from django.utils import timezone
from django.utils.text import format_lazy
from django.utils.translation import gettext_lazy as _


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


class Event(models.Model):
    name = models.CharField(_('name'), max_length=25)
    start = models.DateTimeField(_('start date/time'))
    end = models.DateTimeField(_('end date/time'), )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('event')
        verbose_name_plural = _('events')


class EventCheck(models.Model):
    event = models.ForeignKey('Event', verbose_name=_('event'), on_delete=models.CASCADE)
    member_name = models.CharField(_('member name'), max_length=300)
    member_email = models.EmailField(_('member email'), max_length=300)
    entrance_date = models.DateTimeField(_('entrance date/time'),auto_now_add=True)
    exit_date = models.DateTimeField(_('exit date/time'), null=True)

    @property
    def time_passed(self):
        return self.exit_date-self.entrance_date if self.exit_date else None

    def __str__(self):
        text = _('permanence time')
        passed = format_lazy('{text}: {time}', text=text, time=self.time_passed)
        if not self.time_passed:
            passed = _('not checked out')
        return f'{self.member_name} - {passed}'

    def checkout(self, date=timezone.now()):
        delta_event = self.event.end - self.event.start
        delta_check = date - self.entrance_date
        result = delta_check.seconds * 100 / delta_event.seconds

        self.exit_date = date
        self.save()

        return result >= 75

    class Meta:
        verbose_name = _('event check')
        verbose_name_plural = _('event checks')
