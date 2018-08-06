from django import conf

from io import BytesIO
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


def generate_certificate(name, cpf=None):
    # TODO: there's gotta be a better way!
    font_path = Path(conf.settings.BASE_DIR) / 'assets' / 'Oswald-Regular.ttf'
    font_path_cpf = Path(conf.settings.BASE_DIR) / 'assets' / 'Montserrat-Medium.ttf'
    certificate_path = Path(conf.settings.BASE_DIR) / 'assets' / 'certificate_model.png'
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
        cpf_text = f'portador(a) do CPF {cpf},'
        w, h = draw.textsize(cpf_text, font_cpf)
        draw.text(((im.width - w) / 2, (im.height + 130 - h) / 2), cpf_text, font=font_cpf, fill="#3F404B")

    output = BytesIO()
    im.convert("RGB").save(output, format='PDF')
    output.seek(0)
    return output
