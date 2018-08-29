# Create your views here.
from datetime import timedelta

from django.db.models import Q
from django.utils import timezone
from rest_framework import viewsets, generics
from rest_framework.views import *
from django.shortcuts import *
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions

from api import senders
from api.models import MemberInfo, EventDayCheck, Event, Attendee
from api.serializers import MemberInfoSerializer, EventCheckSerializer, EventSerializer, AttendeeSerializer
from api import permissions


class MemberInfoViewSet(viewsets.ViewSet):
    """
    API endpoint that allows members to be registered.
    """
    serializer_class = MemberInfoSerializer
    queryset = None

    def create(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            try:
                member_info = MemberInfo(**serializer.validated_data)
                senders.send_registration_mail(member_info)
                return Response(serializer.validated_data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({
                    'status': 'Server error',
                    'message': 'Error at sending e-mail. Please try again.'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({
            'status': 'Bad request',
            'message': 'Member could not be created with received data.'
        }, status=status.HTTP_400_BAD_REQUEST)


class EventCheckView(APIView):
    """
    API endpoint that allows members to check in and out of events.
    """

    # def post(self, request, format=None):
    #     serializer = EventCheckSerializer(data=request.data)
    #     if serializer.is_valid():
    #         now = timezone.now()
    #         delta = timedelta(minutes=60)
    #         now_plus = now + delta
    #         now_minus = now - delta
    #
    #         queryset = Event.objects.filter(
    #             (Q(start__lte=now) & Q(end__gte=now)) |
    #             (Q(start__lte=now_plus) & Q(end__gte=now)) |
    #             (Q(start__lte=now) & Q(end__gte=now_minus)),
    #             id=serializer.data['event']
    #         )
    #
    #         if queryset.all():
    #             if serializer.data['check']:
    #                 return self.checkin(serializer.data)
    #             return self.checkout(serializer.data)
    #         else:
    #             return Response({'status': 'BAD_REQUEST', 'message': 'Event inactive.'},
    #                             status=status.HTTP_400_BAD_REQUEST)
    #
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #
    # def checkin(self, data):
    #     check = EventDayCheck.objects.filter(event_id=data['event'],
    #                                       member_name=data['member']['name'],
    #                                       member_email=data['member']['email']).first()
    #     if check:
    #         return Response({'status': 'BAD_REQUEST', 'message': 'Member already checked-in.'},
    #                         status=status.HTTP_400_BAD_REQUEST)
    #
    #     EventCheck(event_id=data['event'],
    #                member_name=data['member']['name'],
    #                member_email=data['member']['email']).save()
    #     return Response(data, status=status.HTTP_201_CREATED)
    #
    # def checkout(self, data):
    #     check = EventCheck.objects.filter(event_id=data['event'],
    #                                       member_name=data['member']['name'],
    #                                       member_email=data['member']['email']).first()
    #     if not check:
    #         return Response({'status': 'BAD_REQUEST', 'message': 'Member did not checkin.'},
    #                         status=status.HTTP_400_BAD_REQUEST)
    #     elif check.exit_date is not None:
    #         return Response({'status': 'BAD_REQUEST', 'message': 'Member already checked-out.'},
    #                         status=status.HTTP_400_BAD_REQUEST)
    #
    #     if check.checkout():
    #         senders.send_certificate_mail(data['member']['name'], data['member']['email'],
    #                                       cpf=data['member'].get('cpf', None))
    #     else:
    #         senders.send_no_certificate_mail(data['member']['name'], data['member']['email'])
    #
    #     return Response(data, status=status.HTTP_200_OK)


class CurrentEventView(APIView):
    """
    API endpoint that shows current events.
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        now = timezone.now()
        delta = timedelta(minutes=60)
        now_plus = now + delta
        now_minus = now - delta
        events = Event.objects.filter(
            (Q(start__lte=now) & Q(end__gte=now)) |
            (Q(start__lte=now_plus) & Q(end__gte=now)) |
            (Q(start__lte=now) & Q(end__gte=now_minus))
        ).all()
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
