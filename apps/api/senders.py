import base64
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.translation import gettext as _

from apps.api.qrcode import gen_qrcode
from .models import Attendee, Event


def send_registration_mail(attendee: Attendee, event: Event):
    qr_data = gen_qrcode(data=str(attendee.uuid)).read()
    
    subject = f"Inscrição Confirmada - {event.name}"
    from_email = "GruPy-RN <coordenacao@grupyrn.org>"
    to_email = [attendee.email]
    
    context = {
        'first_name': attendee.name.split()[0],
        'event_name': event.name,
    }
    
    html_content = render_to_string('api/email/registration.html', context)
    text_content = f"Olá {context['first_name']}, sua inscrição no {context['event_name']} foi confirmada. Credencial em anexo."

    msg = EmailMultiAlternatives(subject, text_content, from_email, to_email)
    msg.attach_alternative(html_content, "text/html")
    
    # Attach QR Code
    # qr_data is bytes
    msg.attach('credencial_grupyrn.png', qr_data, 'image/png')
    
    try:
        msg.send()
        return qr_data
    except Exception as e:
        raise e


def send_certificate_mail(name, email, event, cpf=None):
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
    
    subject = f"Certificado - {event.name}"
    from_email = "GruPy-RN <coordenacao@grupyrn.org>"
    to_email = [email]
    
    context = {
        'first_name': name.split()[0],
        'event_name': event.name,
    }

    html_content = render_to_string('api/email/certificate_emitted.html', context)
    text_content = f"Olá {context['first_name']}, seu certificado do {context['event_name']} está pronto. Veja em anexo."

    msg = EmailMultiAlternatives(subject, text_content, from_email, to_email)
    msg.attach_alternative(html_content, "text/html")

    # Attach PDF
    # certificate_data is usually a BytesIO or similar file-like object
    msg.attach('certificado.pdf', certificate_data.read(), 'application/pdf')

    try:
        msg.send()
        return True
    except Exception as e:
        # Compatibility with old behavior: print error and re-raise
        print(str(e))
        raise e


def send_no_certificate_mail(name, email, event):
    subject = f"Certificado - {event.name}"
    from_email = "GruPy-RN <coordenacao@grupyrn.org>"
    to_email = [email]
    
    context = {
        'first_name': name.split()[0],
        'event_name': event.name,
    }

    html_content = render_to_string('api/email/certificate_not_emitted.html', context)
    text_content = f"Olá {context['first_name']}, infelizmente você não atingiu a frequência mínima para o certificado do {context['event_name']}."

    msg = EmailMultiAlternatives(subject, text_content, from_email, to_email)
    msg.attach_alternative(html_content, "text/html")

    try:
        msg.send()
        return True
    except Exception as e:
        print(str(e))
        raise e
