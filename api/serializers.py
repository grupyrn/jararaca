from api.models import Event
from registration.validators import cpf_validator
from rest_framework import serializers


class MemberInfoSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=200)
    email = serializers.EmailField()
    cpf = serializers.CharField(max_length=11, required=False, validators=[cpf_validator])


class EventCheckSerializer(serializers.Serializer):
    member = MemberInfoSerializer()
    check = serializers.BooleanField()
    event = serializers.PrimaryKeyRelatedField(queryset=Event.objects.all())


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ('id', 'name', 'start', 'end')
