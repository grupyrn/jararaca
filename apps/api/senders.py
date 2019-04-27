import base64

from django.conf import settings
from django.utils.translation import gettext as _
from sendgrid import *
from sendgrid.helpers.mail import *

from apps.api.qrcode import gen_qrcode
from .models import Attendee, Event

sg = sendgrid.SendGridAPIClient(apikey=settings.SENDGRID_API_KEY)
templates = settings.SENDGRID_TEMPLATES


def send_registration_mail(attendee: Attendee, event: Event):
    qr_data = gen_qrcode(data=str(attendee.uuid)).read()
    template = templates['REGISTRATION']

    mail = Mail()
    mail.from_email = Email(template['FROM_EMAIL'], template['FROM_NAME'])
    mail.template_id = template['ID']
    mail.add_category(Category(template['CATEGORY']))

    attachment1 = Attachment()
    attachment1.content = base64.b64encode(qr_data).decode('ascii')
    attachment1.filename = template['FILENAME']
    mail.add_attachment(attachment1)

    personalization = Personalization()
    personalization.add_substitution(Substitution("%first_name%", attendee.name.split()[0]))
    personalization.add_substitution(Substitution("%event_name%", event.name))
    personalization.add_to(Email(attendee.email, attendee.name))
    mail.add_personalization(personalization)

    try:
        sg.client.mail.send.post(request_body=mail.get())
        return qr_data
    except Exception as e:
        raise e


def send_certificate_mail(name, email, event, cpf=None):
    template = templates['CERTIFICATE_EMITTED']

    mail = Mail()
    mail.from_email = Email(template['FROM_EMAIL'], template['FROM_NAME'])
    mail.template_id = template['ID']
    mail.add_category(Category(template['CATEGORY']))

    attachment1 = Attachment()

    if isinstance(event, Event):
        event_place = event.place
        event_duration = event.formated_duration
        event_date = event.formated_dates
        event_min_percent = event.certificate_minimum_time
    else:
        event_place = event.event_day.event.place
        event_duration = event.event_day.event.formated_duration
        event_date = event.event_day.event.formated_dates
        event_min_percent = event.event_day.event.certificate_minimum_time


    cpf_text = _(', bearer of the registry number %(cpf)s,') % {'cpf': cpf} if cpf else ''
    data = {'name': name, 'event': event.name, 'cpf': cpf_text, 'event_date': event_date,
            'event_place': event_place, 'event_duration': event_duration,
            'event_min_percent': event_min_percent}

    certificate_data = event.certificate_model.generate_certificate(data)

    attachment1.content = base64.b64encode(certificate_data.read()).decode('ascii')
    attachment1.filename = template['FILENAME']
    mail.add_attachment(attachment1)

    personalization = Personalization()
    personalization.add_substitution(Substitution("%first_name%", name.split()[0]))
    personalization.add_substitution(Substitution("%event_name%", event.name))
    personalization.add_to(Email(email, name))
    mail.add_personalization(personalization)

    try:
        response = sg.client.mail.send.post(request_body=mail.get())
        return True
    except Exception as e:
        print(e.body)
        raise e


def send_no_certificate_mail(name, email, event):
    template = templates['CERTIFICATE_NOT_EMITTED']

    mail = Mail()
    mail.from_email = Email(template['FROM_EMAIL'], template['FROM_NAME'])
    mail.template_id = template['ID']
    mail.add_category(Category(template['CATEGORY']))

    personalization = Personalization()
    personalization.add_substitution(Substitution("%first_name%", name.split()[0]))
    personalization.add_substitution(Substitution("%event_name%", event.name))
    personalization.add_to(Email(email, name))
    mail.add_personalization(personalization)

    try:
        response = sg.client.mail.send.post(request_body=mail.get())
        return True
    except Exception as e:
        print(e.body)
        raise e
