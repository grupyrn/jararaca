from django.conf import settings

from jararaca import settings as jararaca_settings


def pytest_configure():
    settings.configure(LANGUAGE_CODE='pt-BR')
