from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import User 
from .models import Event

class EventNotificationLogicTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.now = timezone.now()

    
    
    def test_notification_for_upcoming_event(self):
        event = Event.objects.create(
            user=self.user, 
            title="Скоро начнется",
            event_datetime=self.now + timedelta(hours=2)
        )
        self.assertTrue(event.should_send_notification())

    def test_no_notification_for_distant_event(self):
        event = Event.objects.create(
            user=self.user, 
            title="Еще долго ждать",
            event_datetime=self.now + timedelta(hours=25)
        )
        self.assertFalse(event.should_send_notification())

    def test_no_notification_for_past_event(self):
        event = Event.objects.create(
            user=self.user, 
            title="Уже прошло",
            event_datetime=self.now - timedelta(hours=1)
        )
        self.assertFalse(event.should_send_notification())

    def test_notification_at_exactly_24_hours(self):
        event = Event.objects.create(
            user=self.user, 
            title="Граничный случай",
            event_datetime=self.now + timedelta(hours=24)
        )
        self.assertTrue(event.should_send_notification())

    def test_return_type(self):
        event = Event.objects.create(
            user=self.user, 
            title="Тип данных",
            event_datetime=self.now + timedelta(hours=1)
        )
        self.assertIsInstance(event.should_send_notification(), bool)

    def test_database_integrity(self):
        Event.objects.create(
            user=self.user, 
            title="Интеграция",
            event_datetime=self.now + timedelta(hours=10)
        )
        self.assertEqual(Event.objects.filter(title="Интеграция").count(), 1)