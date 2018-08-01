# -*- coding: utf-8 -*-

from rest_framework import serializers
from django.conf import settings


def cpf_validator(value):
    if len(value) != 11 or len(set(value)) == 1:
        raise serializers.ValidationError(ExceptionMessage.invalid_cpf())

    first_cpf_weight = [10, 9, 8, 7, 6, 5, 4, 3, 2]
    second_cpf_weight = [11, 10, 9, 8, 7, 6, 5, 4, 3, 2]
    first_part = value[:9]
    first_digit = value[9]
    second_digit = value[10]

    if not ((first_digit == Utils.get_first_digit(number=first_part, weight=first_cpf_weight)
             and second_digit == Utils.get_second_digit(updated_number=value[:10], weight=second_cpf_weight))):
        raise serializers.ValidationError(ExceptionMessage.invalid_cpf())


class Utils:

    DIVIDER = 11

    @staticmethod
    def get_first_digit(number, weight):
        sum = 0

        for i in range(len(weight)):
            sum += int(number[i]) * weight[i]

        rest_division = sum % Utils.DIVIDER

        if rest_division < 2:
            return '0'

        return str(11 - rest_division)

    @staticmethod
    def get_second_digit(updated_number, weight):
        sum = 0

        for i in range(len(weight)):
            sum += + int(updated_number[i]) * weight[i]

        rest_division = sum % Utils.DIVIDER

        if rest_division < 2:
            return '0'

        return str(11 - rest_division)


class ExceptionMessage:
    LANGUAGE_CODE = settings.LANGUAGE_CODE

    translations = [
        {'lang': 'en-US', 'message-cpf': 'Invalid CPF', 'message-cnpj': 'Invalid CNPJ'},
        {'lang': 'pt-BR', 'message-cpf': 'CPF inválido', 'message-cnpj': 'CNPJ inválido'},
        {'lang': 'es-ES', 'message-cpf': 'CPF no válido', 'message-cnpj': 'CNPJ no válido'},
    ]

    @staticmethod
    def invalid_cpf():
        for tr in ExceptionMessage.translations:
            if tr['lang'] == ExceptionMessage.LANGUAGE_CODE:
                return tr['message-cpf']

    @staticmethod
    def invalid_cnpj():
        for tr in ExceptionMessage.translations:
            if tr['lang'] == ExceptionMessage.LANGUAGE_CODE:
                return tr['message-cnpj']
