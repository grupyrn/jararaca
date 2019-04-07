from django.contrib import admin, messages
from django.db.models import F
from django.http import HttpResponse
from django.urls import reverse
from django.utils.formats import date_format
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

# Register your models here.
from apps.api import senders
from apps.api.exporters import generate_xlsx
from apps.api.models import Event, EventDayCheck, EventSchedule, EventDay, Attendee, SubEventCheck, SubEvent, \
    CertificateModel

admin.site.site_header = _("Jararaca - GruPy-RN Event and Check-in System")


@admin.register(EventDayCheck)
class EventDayCheckAdmin(admin.ModelAdmin):
    list_filter = ('event_day__event__name',)
    search_fields = ('attendee__name', 'attendee__email', 'attendee__cpf')
    list_display = ('attendee_name', 'event', 'entrance_date', 'exit_date', 'time_passed')
    readonly_fields = ('event_day', 'attendee', 'entrance_date', 'exit_date', 'time_passed')

    def get_queryset(self, request):
        qs = super(EventDayCheckAdmin, self).get_queryset(request)
        if not request.user.is_superuser:
            qs = qs.filter(event_day__event__created_by=request.user)
        return qs


class EventScheduleInline(admin.StackedInline):
    model = EventSchedule
    extra = 1
    ordering = ('start',)


class EventDayInline(admin.TabularInline):
    model = EventDay
    extra = 1
    fields = ['date', 'start', 'end', 'schedule_link']
    readonly_fields = ('schedule_link',)


@admin.register(EventDay)
class EventDayAdmin(admin.ModelAdmin):
    inlines = [
        EventScheduleInline,
    ]

    def get_queryset(self, request):
        qs = super(EventDayAdmin, self).get_queryset(request)
        if not request.user.is_superuser:
            qs = qs.filter(event__created_by=request.user)
        return qs


@admin.register(Attendee)
class AttendeeAdmin(admin.ModelAdmin):
    list_filter = ('event', 'share_data_with_partners')
    list_display = ('name', 'event', 'date', 'eventdaycheck_link')
    search_fields = ('name', 'email', 'cpf')
    readonly_fields = ('uuid', 'event', 'name', 'email', 'cpf', 'share_data_with_partners',
                       'formated_presence_percentage', 'is_eligible_to_certificate', 'eventdaycheck_link')
    actions = ['generate_xlsx', 'send_certificate']

    def get_queryset(self, request):
        qs = super(AttendeeAdmin, self).get_queryset(request)
        if not request.user.is_superuser:
            qs = qs.filter(event__created_by=request.user)
        return qs

    def generate_xlsx(self, request, queryset):
        response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        response['Content-Disposition'] = f"attachment; filename=participantes.xlsx"
        xlsx_file = generate_xlsx(response, queryset, ['event', 'name', 'email', 'share_data_with_partners'])
        return response

    generate_xlsx.short_description = _('Generate XLSX spreadsheet')

    def send_certificate(self, request, queryset):
        for attendee in queryset.all():
            if attendee.presence_percentage >= attendee.event.certificate_minimum_time:
                senders.send_certificate_mail(attendee.name, attendee.email, attendee.event,
                                              cpf=attendee.cpf)
        messages.add_message(request, messages.INFO, _('The certficates were successfuly sent to the eligible '
                                                       'selected attendees.'))

    send_certificate.short_description = _('Send certificate')

    @mark_safe
    def eventdaycheck_link(self, obj):
        chk = obj.eventdaycheck_set
        if chk:
            html = ''
            for check in obj.eventdaycheck_set.all():
                changeform_url = reverse(
                    'admin:api_eventdaycheck_change', args=(check.id,)
                )
                html += '<a href="%s">%s</a> ' % (
                    changeform_url, date_format(check.event_day.date, format='SHORT_DATE_FORMAT', use_l10n=True))
            return html
        return u''

    eventdaycheck_link.short_description = _('Check-in')

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    exclude = ('created_by',)
    inlines = [
        EventDayInline,
    ]

    def get_queryset(self, request):
        qs = super(EventAdmin, self).get_queryset(request)
        if not request.user.is_superuser:
            qs = qs.filter(created_by=request.user)
        return qs

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'created_by', None) is None:
            obj.created_by = request.user
        obj.save()


@admin.register(SubEvent)
class SubEventAdmin(admin.ModelAdmin):
    list_display = ('title', 'event_day',)
    list_filter = ('event_day',)


@admin.register(SubEventCheck)
class SubEventCheckAdmin(admin.ModelAdmin):
    list_display = ('attendee_name', 'subevent', 'entrance_date', 'exit_date')
    list_filter = ('subevent',)
    actions = ['generate_xlsx']

    def generate_xlsx(self, request, queryset):
        queryset = queryset.annotate(name=F('attendee__name'), email=F('attendee__email'), cpf=F('attendee__cpf'))
        response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        response['Content-Disposition'] = f"attachment; filename=participantes_subeventos.xlsx"
        xlsx_file = generate_xlsx(response, queryset, ['name', 'subevent', 'email', 'cpf'])
        return response

    generate_xlsx.short_description = _('Generate XLSX spreadsheet')


@admin.register(CertificateModel)
class CertificateModelAdmin(admin.ModelAdmin):
    list_display = ('name',)
    readonly_fields = ('preview',)
