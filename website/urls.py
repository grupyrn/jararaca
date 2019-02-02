from django.urls import path
from .views import *

urlpatterns = [
    path('', WelcomeView.as_view(), name='home'),
    path('rules', Rule.as_view(), name='rules'),
    path('<slug:event>', EventInfoView.as_view(), name='event-info'),
    path('<slug:event>/register', AttendeeRegistrationView.as_view(), name='attendee-registration'),
]
