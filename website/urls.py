from django.urls import path
from .views import *

urlpatterns = [
    # path('', AttendeeRegistrationView.as_view()),
    path('', WelcomeView.as_view()),
    path('registration', AttendeeRegistrationView.as_view(), name='form'),
]
