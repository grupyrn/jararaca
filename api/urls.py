from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from .views import *

router = routers.DefaultRouter()
router.register(r'members', MemberInfoViewSet, base_name='members')

urlpatterns = [
    path('', include(router.urls)),
    path('check/', EventCheckView.as_view()),
    path('currentevent/', CurrentEventView.as_view()),
]
