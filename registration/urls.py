from django.urls import path
from .views import *

urlpatterns = [
    path('', MemberRegistrationView.as_view()),
]
