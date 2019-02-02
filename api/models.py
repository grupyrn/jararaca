import json
import traceback
import uuid
from datetime import date, datetime, timedelta
from io import BytesIO

from PIL import Image
from colorful.fields import RGBColorField
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Q
from django.urls import reverse
from django.utils import timezone
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.utils.text import format_lazy
from django.utils.translation import gettext_lazy as _

from api.helpers import date_range_format, scale_to_width


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

    @property
    def presence_percentage(self):
        event_time = 0
        for day in self.event.eventday_set.all():
            event_time += (datetime.combine(date.min, day.end) - datetime.combine(date.min, day.start)).seconds

        checked_time = 0
        for checked_day in self.eventdaycheck_set.filter(exit_date__isnull=False):
            checked_time += (checked_day.exit_date - checked_day.entrance_date).seconds

        result = checked_time * 100 / event_time

        return result

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
    content_link = models.URLField(_('content link'), null=True, blank=True)
    certificate_model = models.ForeignKey('CertificateModel', verbose_name=_('certificate model'), null=True,
                                          blank=True, on_delete=models.PROTECT)
    certificate_hours = models.IntegerField(_('certificate hours'), default=4)
    closed_registration = models.BooleanField(_('closed registration'), default=False)

    @property
    def formated_duration(self):
        hours = self.certificate_hours
        return f'{hours} horas' if hours != 1 else f'{hours} hora'

    @property
    def formated_dates(self):
        dates = self.eventday_set.values_list('date', flat=True)
        return date_range_format(dates)

    @property
    def date(self):
        return self.eventday_set.order_by('date').values_list('date', flat=True).all()

    @property
    def start(self):
        day = self.eventday_set.order_by('date').first()
        return datetime.combine(day.date, day.start)

    @property
    def end(self):
        day = self.eventday_set.order_by('-date').first()
        return datetime.combine(day.date, day.end)

    @property
    def current_day(self):
        return self.eventday_set.get(date=date.today())

    @staticmethod
    def current_events(tolerance: timedelta):
        now = datetime.now()
        tolerance = timedelta(minutes=60)
        now_plus = now + tolerance
        now_minus = now - tolerance

        return Event.objects.filter(
            (Q(eventday__date=now.date()) & Q(eventday__start__lte=now.time()) & Q(eventday__end__gte=now.time())) |
            (Q(eventday__date=now.date()) & Q(eventday__start__lte=now_plus.time()) & Q(
                eventday__end__gte=now.time())) |
            (Q(eventday__date=now.date()) & Q(eventday__start__lte=now.time()) & Q(eventday__end__gte=now_minus.time()))
        )

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

    @property
    def is_last(self):
        return self == self.event.eventday_set.latest('date')

    @mark_safe
    def schedule_link(self):
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
        unique_together = ('event', 'date')


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
        ordering = ['start']


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

    class Meta:
        verbose_name = _('event day check')
        verbose_name_plural = _('event day checks')


class SubEvent(models.Model):
    event_day = models.ForeignKey('EventDay', verbose_name=_('event day'), on_delete=models.CASCADE)
    start = models.TimeField(_('start time'))
    end = models.TimeField(_('end time'))
    title = models.CharField(_('title'), max_length=150)
    certificate_model = models.ForeignKey('CertificateModel', verbose_name=_('certificate model'), null=True,
                                          blank=True, on_delete=models.PROTECT)
    certificate_hours = models.IntegerField(_('certificate hours'), default=4)

    @property
    def name(self):
        return self.title

    @property
    def formated_duration(self):
        hours = self.certificate_hours
        return f'{hours} horas' if hours != 1 else f'{hours} hora'

    @property
    def formated_dates(self):
        dates = [self.event_day.date]
        return date_range_format(dates)

    @property
    def is_active(self):
        today = date.today()
        now = datetime.now().time()
        return today == self.event_day.date and self.start < now < self.end

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('subevent')
        verbose_name_plural = _('subevents')
        ordering = ['start']


class SubEventCheck(models.Model):
    attendee = models.ForeignKey('Attendee', verbose_name=_('attendee'), on_delete=models.CASCADE)
    subevent = models.ForeignKey('SubEvent', verbose_name=_('subevent'), on_delete=models.CASCADE)
    entrance_date = models.DateTimeField(_('entrance date/time'), null=True, blank=True)
    exit_date = models.DateTimeField(_('exit date/time'), null=True, blank=True)

    @property
    def attendee_name(self):
        return self.attendee.name

    class Meta:
        verbose_name = _('subevent check')
        verbose_name_plural = _('subevent checks')


class CertificateModel(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(_('certificate image'), help_text=_('Image sized 2000x1545'))
    text = models.TextField(_('text'))
    font = models.FileField(_('font'), help_text=_('TrueType font file'))
    font_size = models.IntegerField(_('font size'))
    font_color = RGBColorField(_('font color'))
    alignment = models.CharField(_('alignment'), max_length=10,
                                 choices=[('left', _('Left')), ('right', _('Right')), ('center', _('Center')),
                                          ('justify', _('Justify')), ])
    line_spacing = models.IntegerField(_('line spacing'))
    text_x = models.FloatField(_('text X position'), help_text=_('Percentage from model width'))
    text_y = models.FloatField(_('text Y position'), help_text=_('Percentage from model height'))
    text_width = models.FloatField(_('text width'), help_text=_('Percentage from model width'))

    def preview(self):
        if self.image:
            return format_html('<img src="%s" />' % reverse('preview_certificate', args=(self.id,)))
        else:
            return '-'

    preview.short_description = _('preview')
    preview.allow_tags = True

    def __str__(self):
        return self.name

    def generate_certificate(self, data, preview=False):
        font_path = str(self.font.path)
        im = Image.open(str(self.image.path))

        text_y = im.height * self.text_y / 100
        text_x = im.width * self.text_x / 100
        text_width = im.width * self.text_width / 100

        from api.image_utils import ImageText

        im = ImageText(im)

        if data:
            try:
                text = self.text.format(**data)
            except Exception as e:
                text = self.text
                traceback.print_exc()
        else:
            text = self.text

        im.write_text_box(text_x, text_y, box_width=text_width, font_filename=font_path,
                          text=text, font_size=self.font_size, line_spacing=self.line_spacing,
                          color=self.font_color, place=self.alignment)

        if preview:
            size = scale_to_width(im.image.size, 500)
            b = BytesIO()
            im.image.resize(size, Image.BICUBIC).convert('RGB').save(b, format='PNG')
            b.seek(0)
            return b
        else:
            output = BytesIO()
            im.image.convert("RGB").save(output, format='PDF')
            output.seek(0)
            return output

    class Meta:
        verbose_name = _('certificate model')
        verbose_name_plural = _('certificate models')
