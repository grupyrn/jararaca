import base64
from datetime import date

from django.contrib import messages
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.utils.datastructures import OrderedSet
from django.utils.translation import gettext_lazy as _
from django.views.generic import FormView
from django.views.generic import TemplateView

from apps.api import senders
from apps.api.models import Event, Attendee
from apps.site.forms import AttendeeForm


class WelcomeView(TemplateView):
    template_name = 'site/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['future_events'] = OrderedSet(Event.objects.filter(eventday__date__gte=date.today()).order_by(
            'eventday__date'))
        context['past_events'] = OrderedSet(Event.objects.filter(eventday__date__lte=date.today()).order_by(
            '-eventday__date'))
        return context


class EventInfoView(TemplateView):
    template_name = 'site/event.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context.update(event=get_object_or_404(Event, slug=context['event']))
        return self.render_to_response(context)


class CheckinView(TemplateView):
    template_name = 'site/checkin.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)


class RulesView(TemplateView):
    template_name = 'site/rules.html'


class AttendeeRegistrationView(FormView):
    template_name = 'site/form.html'
    form_class = AttendeeForm

    success_url = '/thanks/'

    def get(self, request, *args, **kwargs):
        event = OrderedSet(Event.objects.filter(slug=kwargs['event'], eventday__date__gte=date.today(),
                                                closed_registration=False))
        if not len(event):
            raise Http404

        event = list(event)[0]

        return self.render_to_response(self.get_context_data(event=event))

    def form_valid(self, form):
        event = OrderedSet(Event.objects.filter(slug=self.request.POST['event'], eventday__date__gte=date.today(),
                                                closed_registration=False))
        if not len(event):
            raise Http404

        event = list(event)[0]

        attendee = form.instance
        attendee.event = event
        defaults = form.cleaned_data
        authorize = defaults.pop('authorize')
        
        if not authorize:
            messages.error(self.request, _('Registration failed.'))
            return self.form_invalid(form)

        user, created = Attendee.objects.get_or_create(
            event=event,
            email=attendee.email,
            defaults=form.cleaned_data
        )
        try:
            qr_data = senders.send_registration_mail(user, event)
            context = self.get_context_data(qr_code=base64.b64encode(qr_data).decode('ascii'))
            if created:
                return render(self.request, 'site/thanks.html', context)
            return render(self.request, 'site/duplicate.html', context)
        
        except Exception as e:
            print(e)
            messages.error(self.request, _('Registration failed.'))
            return self.form_invalid(form)

    def form_invalid(self, form):
        event = OrderedSet(Event.objects.filter(slug=self.request.POST['event'], eventday__date__gte=date.today(),
                                                closed_registration=False))
        if not len(event):
            raise Http404
        event = list(event)[0]
        return self.render_to_response(self.get_context_data(form=form, event=event))
