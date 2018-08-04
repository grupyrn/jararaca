import base64
from io import BytesIO
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
from cryptography.fernet import Fernet
from django import conf

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


def send_certificate(name, email, cpf=None):
    font_path = Path(conf.settings.BASE_DIR) / 'assets' / 'Oswald-Regular.ttf'
    font_path_cpf = Path(conf.settings.BASE_DIR) / 'assets' / 'Montserrat-Medium.ttf'
    certificate_path = Path(conf.settings.BASE_DIR) / 'assets' / 'modelo_certificado.png'
    font = ImageFont.truetype(str(font_path), size=70)
    font_cpf = ImageFont.truetype(str(font_path_cpf), size=45)

    im = Image.open(certificate_path)

    draw = ImageDraw.Draw(im)
    if not cpf:
        w, h = draw.textsize(name, font)
        draw.text(((im.width - w) / 2, (im.height+20 - h) / 2), name, font=font, fill="#3F404B")
    else:
        w, h = draw.textsize(name, font)
        draw.text(((im.width - w) / 2, (im.height - 50 - h) / 2), name, font=font, fill="#3F404B")
        cpf_text = f'portador do CPF {cpf},'
        w, h = draw.textsize(cpf_text, font_cpf)
        draw.text(((im.width - w) / 2, (im.height + 130 - h) / 2), cpf_text, font=font_cpf, fill="#3F404B")

    # im.convert("RGB").save('teste.pdf', format='PDF')

    output = BytesIO()
    im.convert("RGB").save(output, format='PDF')
    output.seek(0)

    mail = Mail()
    mail.from_email = Email("coordenacao@grupyrn.org", "GruPy-RN")
    mail.template_id = "f26688fc-1854-455a-a2c0-bd72d2a38b56"
    mail.add_category(Category("certificados_grupy"))

    attachment1 = Attachment()
    attachment1.content = base64.b64encode(output.read()).decode('ascii')
    attachment1.filename = "certificado_3_meetup.pdf"
    mail.add_attachment(attachment1)

    personalization = Personalization()
    personalization.add_substitution(Substitution("%first_name%", name.split()[0]))
    personalization.add_to(Email(email, name))
    mail.add_personalization(personalization)

    try:
        response = sg.client.mail.send.post(request_body=mail.get())
        return True
    except Exception as e:
        print(e.body)
        raise e


def send_no_certificate(name, email):
    mail = Mail()
    mail.from_email = Email("coordenacao@grupyrn.org", "GruPy-RN")
    mail.template_id = "637c0650-3dec-4505-a006-8b9149b3cce4"
    mail.add_category(Category("sem_certificados_grupy"))

    personalization = Personalization()
    personalization.add_substitution(Substitution("%first_name%", name.split()[0]))
    personalization.add_to(Email(email, name))
    mail.add_personalization(personalization)

    try:
        response = sg.client.mail.send.post(request_body=mail.get())
        return True
    except Exception as e:
        print(e.body)
        raise e





