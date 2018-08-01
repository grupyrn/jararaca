from pyqrcode import QRCode
from PIL import Image
from io import BytesIO
from django import conf
from pathlib import Path
import base64


def gen_qrcode(data):
    # Create QRCode
    qrcode = QRCode(data, error='H')

    b64 = qrcode.png_as_base64_str(scale=10)

    # Logo overlay
    qrcode = Image.open(BytesIO(base64.b64decode(b64)))
    qrcode = qrcode.convert("RGBA")
    filepath = Path(conf.settings.BASE_DIR) / 'assets' / 'logo.png'
    logo = Image.open(filepath)
    box = (135, 135, 235, 235)
    qrcode.crop(box)
    logo = logo.resize((box[2] - box[0], box[3] - box[1]))
    logo_width, logo_height = logo.size
    qr_width, qr_height = qrcode.size
    qrcode.paste(logo, ((qr_width-logo_width)//2, (qr_height-logo_height)//2))
    output = BytesIO()
    qrcode.save(output, format="PNG")
    output.seek(0)
    return output
