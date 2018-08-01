# Create your views here.
import base64
import json

from cryptography.fernet import Fernet
from django.conf import settings
from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from sendgrid import *
from sendgrid.helpers.mail import *
from django.views.generic import FormView

from registration.forms import MemberForm
from registration.models import MemberInfo
from registration.serializers import MemberInfoSerializer
from .qrcode import gen_qrcode

sg = sendgrid.SendGridAPIClient(apikey=settings.SENDGRID_API_KEY)


class MemberInfoViewSet(viewsets.ViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    serializer_class = MemberInfoSerializer
    queryset = None

    def create(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            json_data = json.dumps(serializer.validated_data)
            member_info = MemberInfo(**serializer.validated_data)

            cipher_suite = Fernet(settings.CRYPTO_KEY)
            cipher_text = cipher_suite.encrypt(json_data.encode('utf-8'))

            data = gen_qrcode(data=cipher_text)

            mail = Mail()
            mail.from_email = Email("coordenacao@grupyrn.org", "GruPy-RN")
            mail.template_id = "78d0cc02-7d90-4aa4-b214-d842844131c8"
            mail.add_category(Category("inscricao_grupy"))

            attachment1 = Attachment()
            attachment1.content = base64.b64encode(data.read()).decode('ascii')
            attachment1.filename = "credencial_grupy.png"
            mail.add_attachment(attachment1)

            personalization = Personalization()
            personalization.add_substitution(Substitution("%first_name%", member_info.name.split()[0]))
            personalization.add_to(Email(member_info.email, member_info.name))
            mail.add_personalization(personalization)

            try:
                response = sg.client.mail.send.post(request_body=mail.get())
            except Exception as e:
                return Response({
                    'status': 'Server error',
                    'message': 'Error at sending e-mail. Please try again.'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return Response(serializer.validated_data, status=status.HTTP_201_CREATED)

        return Response({
            'status': 'Bad request',
            'message': 'Member could not be created with received data.'
        }, status=status.HTTP_400_BAD_REQUEST)


class MemberRegistrationView(FormView):
    template_name = 'registration/form.html'
    form_class = MemberForm

    success_url = '/thanks/'

    def form_valid(self, form):
        json_data = json.dumps(form.cleaned_data)
        member_info = MemberInfo(**form.cleaned_data)

        cipher_suite = Fernet(settings.CRYPTO_KEY)
        cipher_text = cipher_suite.encrypt(json_data.encode('utf-8'))

        data = gen_qrcode(data=cipher_text)

        mail = Mail()
        mail.from_email = Email("coordenacao@grupyrn.org", "GruPy-RN")
        mail.template_id = "78d0cc02-7d90-4aa4-b214-d842844131c8"
        mail.add_category(Category("inscricao_grupy"))

        attachment1 = Attachment()
        attachment1.content = base64.b64encode(data.read()).decode('ascii')
        attachment1.filename = "credencial_grupy.png"
        mail.add_attachment(attachment1)

        personalization = Personalization()
        personalization.add_substitution(Substitution("%first_name%", member_info.name.split()[0]))
        personalization.add_to(Email(member_info.email, member_info.name))
        mail.add_personalization(personalization)

        try:
            response = sg.client.mail.send.post(request_body=mail.get())
        except Exception as e:
            return Response({
                'status': 'Server error',
                'message': 'Error at sending e-mail. Please try again.'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return render(self.request, 'registration/thanks.html', self.get_context_data())

    def form_invalid(self, form):
        return super().form_invalid(form)
