from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.contrib.auth.models import Group


class Gender(models.TextChoices):
    MEN = "Мужской"
    WOMEN = "Женский"
    
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(choices=Gender, blank=True, max_length=20)
    
    country = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    street = models.CharField(max_length=100, blank=True)
    house = models.CharField(max_length=100, blank=True)
    apartament_number = models.CharField(max_length=100, blank=True)
    
    
class Avatar(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Пользователь")
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True, blank=True , verbose_name="Группа")
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True , verbose_name="Фото")

    def __str__(self):
        return f"{self.user.username} Аватарка"
    
    class Meta:
        verbose_name = "Фото пользователя"
        verbose_name_plural = "Фото пользователей"
    
    
    


