import base64
from cryptography.fernet import Fernet
from django import conf

from api.qrcode import gen_qrcode
from .models import MemberInfo, Attendee, Event

import json

from sendgrid import *
from sendgrid.helpers.mail import *

from django.conf import settings

sg = sendgrid.SendGridAPIClient(apikey=settings.SENDGRID_API_KEY)


def send_registration_mail(attendee: Attendee, event: Event):
    qr_data = gen_qrcode(data=str(attendee.uuid)).read()

    mail = Mail()
    mail.from_email = Email("coordenacao@grupyrn.org", "GruPy-RN")
    mail.template_id = "78d0cc02-7d90-4aa4-b214-d842844131c8"
    mail.add_category(Category("inscricao_grupy"))

    attachment1 = Attachment()
    attachment1.content = base64.b64encode(qr_data).decode('ascii')
    attachment1.filename = "credencial_grupy.png"
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
    mail = Mail()
    mail.from_email = Email("coordenacao@grupyrn.org", "GruPy-RN")
    mail.template_id = "f26688fc-1854-455a-a2c0-bd72d2a38b56"
    mail.add_category(Category("certificados_grupy"))

    attachment1 = Attachment()


    cpf_text = f', portador(a) do CPF {cpf},' if cpf else ''
    data = {'name': name, 'event': event.name, 'cpf': cpf_text, 'event_date': event.formated_dates,
            'event_place': event.place, 'event_duration': event.formated_duration}
    certificate_data = event.certificate_model.generate_certificate(data)


    attachment1.content = base64.b64encode(certificate_data.read()).decode('ascii')
    attachment1.filename = "certificado.pdf"
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
    mail = Mail()
    mail.from_email = Email("coordenacao@grupyrn.org", "GruPy-RN")
    mail.template_id = "637c0650-3dec-4505-a006-8b9149b3cce4"
    mail.add_category(Category("sem_certificados_grupy"))

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





