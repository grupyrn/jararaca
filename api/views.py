# Create your views here.
from rest_framework import viewsets, authentication
from rest_framework.views import *

from api import senders
from api.models import MemberInfo, EventCheck
from api.serializers import MemberInfoSerializer, EventCheckSerializer


class MemberInfoViewSet(viewsets.ViewSet):
    """
    API endpoint that allows users to be viewed or edited.
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
    authentication_classes = (authentication.TokenAuthentication,)

    def post(self, request, format=None):
        serializer = EventCheckSerializer(data=request.data)
        if serializer.is_valid():
            if serializer.data['check']:
                return self.checkin(serializer.data)
            return self.checkout(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def checkin(self, data):
        check = EventCheck.objects.filter(event_id=data['event'],
                                          member_name=data['member']['name'],
                                          member_email=data['member']['email']).first()
        if check:
            return Response({'status': 'BAD_REQUEST', 'message': 'Member already checked-in.'},
                            status=status.HTTP_400_BAD_REQUEST)

        EventCheck(event_id=data['event'],
                   member_name=data['member']['name'],
                   member_email=data['member']['email']).save()
        return Response(data, status=status.HTTP_201_CREATED)

    def checkout(self, data):
        check = EventCheck.objects.filter(event_id=data['event'],
                                          member_name=data['member']['name'],
                                          member_email=data['member']['email']).first()
        if not check:
            return Response({'status': 'BAD_REQUEST', 'message': 'Member did not checkin.'},
                            status=status.HTTP_400_BAD_REQUEST)
        elif check.exit_date is not None:
            return Response({'status': 'BAD_REQUEST', 'message': 'Member already checked-out.'},
                            status=status.HTTP_400_BAD_REQUEST)

        check.checkout()
        return Response(data, status=status.HTTP_200_OK)
