from django.urls import path
from .views import *

urlpatterns = [
    path('', WelcomeView.as_view()),
    path('form', MemberRegistrationView.as_view(), name='form'),
]
