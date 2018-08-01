import base64

from cryptography.fernet import Fernet

from api.qrcode import gen_qrcode
from .models import MemberInfo

import json

from sendgrid import *
from sendgrid.helpers.mail import *

from django.conf import settings

sg = sendgrid.SendGridAPIClient(apikey=settings.SENDGRID_API_KEY)


def send_registration_mail(member_info: MemberInfo):
    json_data = member_info.to_json()

    cipher_suite = Fernet(settings.CRYPTO_KEY)
    cipher_text = cipher_suite.encrypt(json_data.encode('utf-8'))

    qr_data = gen_qrcode(data=cipher_text).read()

    mail = Mail()
    mail.from_email = Email("coordenacao@grupyrn.org", "GruPy-RN")
    mail.template_id = "78d0cc02-7d90-4aa4-b214-d842844131c8"
    mail.add_category(Category("inscricao_grupy"))

    attachment1 = Attachment()
    attachment1.content = base64.b64encode(qr_data).decode('ascii')
    attachment1.filename = "credencial_grupy.png"
    mail.add_attachment(attachment1)

    personalization = Personalization()
    personalization.add_substitution(Substitution("%first_name%", member_info.name.split()[0]))
    personalization.add_to(Email(member_info.email, member_info.name))
    mail.add_personalization(personalization)

    try:
        sg.client.mail.send.post(request_body=mail.get())
        return qr_data
    except Exception as e:
        raise e
