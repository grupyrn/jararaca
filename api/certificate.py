import locale
from io import BytesIO
from pathlib import Path

from PIL import Image
from django import conf

from api import image_utils
from api.models import SubEvent, Event

print(locale.getlocale(locale.LC_TIME))


def generate_certificate(name, event: Event or SubEvent, cpf=None):
    # TODO: there's gotta be a better way!
    font_path = Path(conf.settings.BASE_DIR) / 'assets' / 'Pontiac-Inline-Shadow.ttf'
    cpf_text = f', portador(a) do CPF {cpf},' if cpf else ''
    if isinstance(event, SubEvent):
        try:
            certificate_path = event.certificate_model.path
        except ValueError:
            certificate_path = event.event_day.event.certificate_model.path
        template = "Certificamos que {name}{cpf} participou da atividade \"{subevent}\" do {event}, realizado na data " \
                   "de {event_date}, nas instalações do {event_place}, com carga horária total de {event_duration}."
        data = {'name': name, 'subevent': event.title, 'event': event.event_day.event.name, 'cpf': cpf_text,
                'event_date': event.formated_dates,
                'event_place': event.event_day.event.place, 'event_duration': event.formated_duration}
    else:
        certificate_path = event.certificate_model.path
        template = "Certificamos que {name}{cpf} participou do {event}, realizado na data de {event_date}, " \
                   "nas instalações do {event_place}, com carga horária total de {event_duration}."
        data = {'name': name, 'event': event.name, 'cpf': cpf_text, 'event_date': event.formated_dates,
                'event_place': event.place, 'event_duration': event.formated_duration}

    im = Image.open(certificate_path)

    text_y = im.height * 0.4
    text_x = im.width * 0.125
    text_width = im.width - text_x * 2

    im = image_utils.ImageText(im)

    text = template.format(**data)

    im.write_text_box(text_x, text_y, box_width=text_width, font_filename=str(font_path),
                      text=text, font_size=52, line_spacing=25, color=(255, 255, 255), place='justify')

    output = BytesIO()
    im.image.convert("RGB").save(output, format='PDF')
    output.seek(0)
    return output
