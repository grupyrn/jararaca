from django.contrib import admin

# Register your models here.
from api.models import Event, EventCheck

admin.site.register(Event)
admin.site.register(EventCheck)
