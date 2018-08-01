from registration.validators import cpf_validator
from .models import MemberInfo
from rest_framework import serializers


class MemberInfoSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=200)
    email = serializers.EmailField()
    cpf = serializers.CharField(max_length=11, required=False, validators=[cpf_validator])
