from django import forms
from django.core import validators
from localflavor.br.forms import BRCPFField


class MemberForm(forms.Form):
    name = forms.CharField(max_length=200)
    email = forms.EmailField()
    cpf = BRCPFField(required=False)
