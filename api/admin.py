from django.contrib import admin
from django.conf import settings

# Register your models here.

from api.models import Event, EventDayCheck, EventSchedule, EventDay

admin.site.site_header = settings.ADMIN_HEADER


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

# admin.site.register(EventDay)
# admin.site.register(EventSchedule)
admin.site.register(EventDayCheck, EventDayCheckAdmin)
