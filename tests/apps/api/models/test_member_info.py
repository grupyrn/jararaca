from apps.api.models import MemberInfo


def test_member_info_to_json_deve_retornar_um_json_valido():
    member_info = MemberInfo(
        name="Joao Maria", email="john.doe@example.com", cpf="11122233344481"
    )
    json_data = member_info.to_json()

    assert json_data == (
        '{"cpf": "11122233344481", '
        '"email": "john.doe@example.com", '
        '"name": "Joao Maria"}'
    )


def test_member_info_to_json_deve_retornar_um_json_valido_quando_um_dos_campos_for_none():  # noqa: E501
    member_info = MemberInfo(
        name="Joao Maria", email="john.doe@example.com", cpf=None
    )
    json_data = member_info.to_json()

    assert json_data == (
        '{"email": "john.doe@example.com", ' '"name": "Joao Maria"}'
    )


def test_member_info_to_json_deve_retornar_um_json_valido_quando_todos_os_campos_for_none():  # noqa: E501
    member_info = MemberInfo(name=None, email=None, cpf=None)
    json_data = member_info.to_json()

    assert json_data == ("{}")
