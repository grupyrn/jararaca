from django.test import TestCase, Client
from django.urls import reverse
from django.utils.datastructures import OrderedSet
from apps.api.models import Event, EventDay
from datetime import date, time


class SiteTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.event = Event.objects.create(
            name="Test Event",
            latitude=0.0,
            longitude=0.0,
            organizers="Test Org",
            slug="test-event"
        )
        EventDay.objects.create(
            event=self.event,
            date=date.today(),
            start=time(9, 0),
            end=time(18, 0)
        )

    def test_home(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_ordered_set(self):
        s = OrderedSet([1, 2, 3])
        self.assertEqual(len(s), 3)
