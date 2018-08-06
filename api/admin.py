from django.contrib import admin
from django.conf import settings

# Register your models here.
from api.models import Event, EventCheck

admin.site.site_header = settings.ADMIN_HEADER


class EventCheckAdmin(admin.ModelAdmin):
    list_filter = ('event__name', )


admin.site.register(Event)
admin.site.register(EventCheck, EventCheckAdmin)
