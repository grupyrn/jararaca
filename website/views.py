# Create your views here.
import base64

from django.shortcuts import render
from django.views.generic import FormView, CreateView
from rest_framework import status
from rest_framework.response import Response
from django.views.generic import TemplateView
from api import senders
from api.models import Event
from website.forms import AttendeeForm
from datetime import date


class WelcomeView(TemplateView):
    template_name = 'website/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['future_events'] = Event.objects.filter(eventday__date__gte=date.today())
        context['past_events'] = Event.objects.filter(eventday__date__lte=date.today())
        return context


class AttendeeRegistrationView(FormView):
    template_name = 'website/form.html'
    form_class = AttendeeForm

    success_url = '/thanks/'

    def form_valid(self, form):
        attendee = form.save()

        try:
            qr_data = senders.send_registration_mail(attendee)
            context = self.get_context_data(qr_code=base64.b64encode(qr_data).decode('ascii'))

            return render(self.request, 'website/thanks.html', context)
        except Exception as e:
            return Response({
                'status': 'Server error',
                'message': 'Error at sending e-mail. Please try again.'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def form_invalid(self, form):
        return super().form_invalid(form)
