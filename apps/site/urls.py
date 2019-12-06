from django.urls import path, re_path
from .views import *

urlpatterns = [
    path('', WelcomeView.as_view(), name='home'),
    path('rules', RulesView.as_view(), name='rules'),
    re_path(r'^check/?((in)|(out)|(message))?$', CheckinView.as_view(), name='checkin'),
    path('<slug:event>', EventInfoView.as_view(), name='event-info'),
    path('<slug:event>/register', AttendeeRegistrationView.as_view(), name='attendee-registration'),
]
