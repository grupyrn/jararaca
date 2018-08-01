from datetime import datetime

from django.db import models


# Create your models here.
class MemberInfo(object):
    def __init__(self, name, email, cpf=None):
        self.name = name
        self.email = email
        self.cpf = cpf
