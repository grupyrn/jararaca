from django import forms
from django.core import validators
from localflavor.br.forms import BRCPFField
from django.utils.translation import gettext_lazy as _
from datetime import date
from api.models import Attendee, Event


class AttendeeForm(forms.ModelForm):
    event = forms.ModelChoiceField(queryset=Event.objects.filter(eventday__date__lte=date.today()))
    cpf = BRCPFField(required=False, help_text=_('Optional. Numbers only. Only if you wish to add this information in '
                                                 'the certificate.'))
    authorize = forms.BooleanField(required=True, label=_('I authorize the use of my data exclusively for my '
                                                          'identification at this GruPy-RN event.'))
    share_data_with_partners = forms.BooleanField(label=_('I also authorize to share my name and e-mail information '
                                                          'with GruPy-RN partners.'))

    class Meta:
        model = Attendee
        fields = ('name', 'email', 'cpf', 'authorize', 'share_data_with_partners')
