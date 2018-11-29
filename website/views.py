import base64

from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from django.views.generic import FormView, CreateView
from django.views.generic import TemplateView
from api import senders
from api.models import Event
from website.forms import AttendeeForm
from datetime import date
from django.utils.translation import gettext_lazy as _


class WelcomeView(TemplateView):
    template_name = 'website/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['future_events'] = Event.objects.filter(eventday__date__gte=date.today())
        context['past_events'] = Event.objects.filter(eventday__date__lte=date.today())
        return context


class EventInfoView(TemplateView):
    template_name = 'website/event.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context.update(event=get_object_or_404(Event, slug=context['event']))
        return self.render_to_response(context)


class AttendeeRegistrationView(FormView):
    template_name = 'website/form.html'
    form_class = AttendeeForm

    success_url = '/thanks/'

    def get(self, request, *args, **kwargs):
        event = get_object_or_404(Event, slug=kwargs['event'], eventday__date__gte=date.today())
        return self.render_to_response(self.get_context_data(event=event))

    def form_valid(self, form):
        event = get_object_or_404(Event, slug=self.request.POST['event'], eventday__date__gte=date.today())

        attendee = form.instance
        attendee.event = event

        try:
            qr_data = senders.send_registration_mail(attendee, event)
            context = self.get_context_data(qr_code=base64.b64encode(qr_data).decode('ascii'))
            attendee.save()

            return render(self.request, 'website/thanks.html', context)
        except Exception as e:
            messages.error(self.request, _('Registration failed.'))
            return self.form_invalid(form)

    def form_invalid(self, form):
        event = get_object_or_404(Event, slug=self.request.POST['event'], eventday__date__gte=date.today())
        return self.render_to_response(self.get_context_data(form=form, event=event))
