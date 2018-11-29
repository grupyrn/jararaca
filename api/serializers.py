from django.utils import timezone
from rest_framework import serializers

from api.models import Event, Attendee, EventDay, EventSchedule, SubEvent
from website.validators import cpf_validator
from datetime import datetime

from django.utils.translation import gettext_lazy as _


class MemberInfoSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=200)
    email = serializers.EmailField()
    cpf = serializers.CharField(max_length=11, required=False, validators=[cpf_validator])


class EventScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventSchedule
        exclude = ['id', 'event']


class EventDaySerializer(serializers.ModelSerializer):
    schedule = EventScheduleSerializer(source='eventschedule_set', many=True)

    class Meta:
        model = EventDay
        fields = ['date', 'schedule']


class EventSerializer(serializers.ModelSerializer):
    days = EventDaySerializer(source='eventday_set', many=True)

    class Meta:
        model = Event
        fields = ['id', 'name', 'description', 'place', 'latitude', 'longitude', 'organizers', 'slug', 'content_link',
                  'days', 'start', 'end']


class AttendeeRegistrationSerializer(serializers.ModelSerializer):
    event = serializers.PrimaryKeyRelatedField(queryset=Event.objects.filter(eventday__date__gte=timezone.now().date()))
    authorize = serializers.BooleanField(required=True, label=_('I authorize the use of my data exclusively for my '
                                                                'identification at this GruPy-RN event.'))

    class Meta:
        model = Attendee
        fields = ['event', 'name', 'email', 'cpf', 'authorize', 'share_data_with_partners']


class AttendeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendee
        fields = ('uuid', 'name', 'email', 'date', 'share_data_with_partners')


class SubEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubEvent
        fields = ['id', 'title', 'event_day']


class EventCheckSerializer(serializers.Serializer):
    attendee = serializers.PrimaryKeyRelatedField(queryset=Attendee.objects)
    check = serializers.BooleanField(required=True)


class SubEventCheckSerializer(serializers.Serializer):
    attendee = serializers.PrimaryKeyRelatedField(queryset=Attendee.objects)
    subevent = serializers.SlugRelatedField(queryset=SubEvent.objects, slug_field='id')
    force = serializers.BooleanField(default=False, required=False)
    check = serializers.BooleanField(required=True)


class SubEventCheckoutSerializer(serializers.Serializer):
    attendee = serializers.PrimaryKeyRelatedField(queryset=Attendee.objects)
