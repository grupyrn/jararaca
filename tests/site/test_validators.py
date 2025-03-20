from rest_framework.serializers import ValidationError
import pytest

from apps.site.validators import cpf_validator, ExceptionMessage


def test_cpf_validator_deve_retornar_none_para_cpf_valido():
    assert cpf_validator('74819936026') is None


def test_cpf_validator_deve_lancar_erro_quando_todos_os_digitos_forem_iguais():
    with pytest.raises(ValidationError):
        cpf_validator('00000000000')


def test_cpf_validator_deve_lancar_erro_quantidade_digitos_for_diferente_de_11():
    with pytest.raises(ValidationError):
        cpf_validator('000000000000')

    with pytest.raises(ValidationError):
        cpf_validator('0000000000')


def test_cpf_validator_deve_lancar_erro_cpf_for_invalido():
    cpf_validator('66511212009')
    cpf_validator('51668260000')
    with pytest.raises(ValidationError):
        cpf_validator('66511212019')


def test_cpf_validator_deve_retornar_none_quando_cpf_for_valido_e_conter_zero_nos_dv():
    assert cpf_validator('66511212009') is None
    assert cpf_validator('51668260000') is None


def test_se_invalid_cpf_retorna_uma_mensagem_de_erro_em_portugues():
    assert ExceptionMessage.invalid_cpf() == 'CPF inválido'


def test_se_invalid_cnpj_retorna_uma_mensagem_de_erro_em_portugues():
    assert ExceptionMessage.invalid_cnpj() == 'CNPJ inválido'
