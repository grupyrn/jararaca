from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from .views import *


urlpatterns = [
    path('previewcertificate/<int:pk>', PreviewCertificateView.as_view(), name='preview_certificate'),
    path('check/', EventCheckView.as_view()),
    path('subeventcheck/', SubEventCheckView.as_view()),
    path('subeventcheckoutall/', SubEventCheckoutAllView.as_view()),
    path('attendees/create/', AttendeeCreateView.as_view()),
    path('attendees/<int:pk>', AttendeeListView.as_view()),
    path('events/', EventListView.as_view()),
    path('subevents/', SubEventListView.as_view()),
    path('currentevents/', CurrentEventsView.as_view()),
]
