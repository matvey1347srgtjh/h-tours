from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

class Event(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    event_datetime = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    # ВОТ ЭТОТ МЕТОД НУЖНО ДОБАВИТЬ ИЛИ ПРОВЕРИТЬ:
    def should_send_notification(self):
        now = timezone.now()
        # Проверяем, что событие наступит в ближайшие 24 часа, но еще не прошло
        return now <= self.event_datetime <= now + timedelta(hours=24)