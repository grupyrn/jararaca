# Create your views here.
from datetime import timedelta

from django.shortcuts import *
from django.utils.translation import gettext as _
from rest_framework import generics, views
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import *

from api import permissions
from api import senders
from api.models import EventDayCheck, Event, Attendee
from api.serializers import AttendeeRegistrationSerializer, EventCheckSerializer, EventSerializer, AttendeeSerializer


class AttendeeCreateView(generics.CreateAPIView):
    """
    API endpoint that allows attendees to be registered.
    """
    queryset = Attendee.objects
    serializer_class = AttendeeRegistrationSerializer


class EventCheckView(views.APIView):
    """
    API endpoint that allows attendees to check in and out of events.
    """

    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        serializer = EventCheckSerializer(data=request.data)
        if serializer.is_valid():

            events = Event.current_events(tolerance=timedelta(minutes=60)).filter(
                id=serializer.validated_data['attendee'].event.id)

            if events.all():
                if serializer.validated_data['check']:
                    return self.checkin(serializer.validated_data)
                return self.checkout(serializer.validated_data)
            else:
                return Response({'status': 'EVENT_INACTIVE', 'message': _('Event inactive.')},
                                status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def checkin(self, data):
        attendee = data['attendee']
        check = EventDayCheck.objects.filter(event_day=attendee.event.current_day,
                                             attendee=attendee).first()

        if check:
            return Response({'status': 'ALREADY_CHECKED_IN',
                             'message': _('%(attendee)s already checked-in.') % {'attendee': attendee.name.split()[0]}},
                            status=status.HTTP_400_BAD_REQUEST)

        EventDayCheck(event_day=attendee.event.current_day,
                      attendee=attendee).save()

        return Response(
            {'status': 'OK',
             'message': _('%(attendee)s successfully checked-in.') % {'attendee': attendee.name.split()[0]},
             'attendee': {
                 'name': attendee.name, 'email': attendee.email
             }},
            status=status.HTTP_201_CREATED)

    def checkout(self, data):
        attendee = data['attendee']
        event_day = attendee.event.current_day
        event_day_check = EventDayCheck.objects.filter(event_day=event_day,
                                                       attendee=attendee).first()

        if not event_day_check:
            return Response({'status': 'NOT_CHECKED_IN',
                             'message': _('%(attendee)s did not checkin.') % {'attendee': attendee.name.split()[0]}},
                            status=status.HTTP_400_BAD_REQUEST)
        elif event_day_check.exit_date is not None:
            return Response({'status': 'ALREADY_CHECKED_OUT',
                             'message': _('%(attendee)s already checked-out.') % {'attendee': attendee.name.split()[0]}},
                            status=status.HTTP_400_BAD_REQUEST)

        event_day_check.checkout()

        if event_day.is_last:
            if attendee.presence_percentage > 75:
                senders.send_certificate_mail(attendee.name, attendee.email, attendee.event,
                                              cpf=attendee.cpf)
            else:
                senders.send_no_certificate_mail(attendee.name, attendee.email, attendee.event)

        return Response(
            {'status': 'OK',
             'message': _('%(attendee)s successfully checked-out.') % {'attendee': attendee.name.split()[0]},
             'attendee': {
                 'name': attendee.name, 'email': attendee.email
             }},
            status=status.HTTP_200_OK)


class CurrentEventsView(APIView):
    """
    API endpoint that shows current events.
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        events = Event.current_events(tolerance=timedelta(minutes=60)).all()
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class EventListView(generics.ListAPIView):
    """
    API endpoint that lists all events.
    """
    queryset = Event.objects
    permission_classes = (IsAuthenticated,)
    serializer_class = EventSerializer


class AttendeeListView(generics.RetrieveAPIView):
    """
    API endpoint that lists all attendees from a specified event.
    """
    queryset = Event.objects
    permission_classes = (IsAuthenticated, permissions.IsOwnerOrSuperUser,)
    serializer_class = AttendeeSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        attendees = get_list_or_404(Attendee, event_id=instance.id)
        serializer = self.get_serializer(attendees, many=True)
        return Response(serializer.data)
