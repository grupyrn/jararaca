# Create your views here.
import base64

from django.shortcuts import render
from django.views.generic import FormView, CreateView
from rest_framework import status
from rest_framework.response import Response

from api import senders
from registration.forms import AttendeeForm


class AttendeeRegistrationView(CreateView):
    template_name = 'registration/form.html'
    form_class = AttendeeForm

    success_url = '/thanks/'

    def form_valid(self, form):
        attendee = form.save()

        try:
            qr_data = senders.send_registration_mail(attendee)
            context = self.get_context_data(qr_code=base64.b64encode(qr_data).decode('ascii'))

            return render(self.request, 'registration/thanks.html', context)
        except Exception as e:
            return Response({
                'status': 'Server error',
                'message': 'Error at sending e-mail. Please try again.'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def form_invalid(self, form):
        return super().form_invalid(form)
