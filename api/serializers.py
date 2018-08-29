from rest_framework import serializers

from api.models import Event, Attendee, EventDay, EventSchedule
from website.validators import cpf_validator


class MemberInfoSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=200)
    email = serializers.EmailField()
    cpf = serializers.CharField(max_length=11, required=False, validators=[cpf_validator])


class EventCheckSerializer(serializers.Serializer):
    member = MemberInfoSerializer()
    check = serializers.BooleanField(required=True)
    event = serializers.PrimaryKeyRelatedField(queryset=Event.objects.all())


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


class AttendeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendee
        fields = ('uuid', 'name', 'email', 'date', 'share_data_with_partners')
