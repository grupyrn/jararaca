from django.contrib import admin
from django.conf import settings
from django.http import HttpResponse
from django.utils.translation import gettext_lazy as _

# Register your models here.
from api.exporters import generate_xlsx
from api.models import Event, EventDayCheck, EventSchedule, EventDay, Attendee

admin.site.site_header = settings.ADMIN_HEADER


@admin.register(EventDayCheck)
class EventDayCheckAdmin(admin.ModelAdmin):
    list_filter = ('event_day__event__name',)
    list_display = ('attendee_name', 'event', 'entrance_date', 'exit_date')

    def get_queryset(self, request):
        qs = super(EventDayCheckAdmin, self).get_queryset(request)
        if not request.user.is_superuser:
            qs = qs.filter(event__created_by=request.user)
        return qs


class EventScheduleInline(admin.StackedInline):
    model = EventSchedule
    extra = 1
    ordering = ('start',)


class EventDayInline(admin.TabularInline):
    model = EventDay
    extra = 1
    fields = ['date', 'start', 'end', 'schedule_link']
    readonly_fields = ('schedule_link', )


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
    list_display = ('name', 'event', 'date', 'share_data_with_partners')
    actions = ['generate_xlsx']

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
