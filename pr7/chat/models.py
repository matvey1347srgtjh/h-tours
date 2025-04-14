from django.db import models
from django.contrib.auth.models import User

class ChatSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_sessions', verbose_name = "Пользователь")
    admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name='admin_sessions', verbose_name = "Асистент поддержки")
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name = "Сессия-Чата"
        verbose_name_plural = "Сессии-Чатов"

    def __str__(self):
        return f"Chat session between {self.user.username} and {self.admin.username}"

class Message(models.Model):
    chat_session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='messages', verbose_name="чат с")
    sender = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Отправитель")
    content = models.TextField(verbose_name="Сообщение")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Время")

    def __str__(self):
        return f"Message from {self.sender.username} at {self.timestamp}"
    
    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"