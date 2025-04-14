from datetime import timedelta
from django.db import models
from django.contrib.auth.models import User
from baza.models import Jewelry

class PaymentStatus(models.TextChoices):
    NOT_STARTED = ('NOT_STARTED', 'Тур еще не начался')
    IN_PROGRESS = ('IN_PROGRESS', 'Тур в процессе')
    COMPLETED = ('COMPLETED', 'Тур закончен')

class Order(models.Model):
    customer_user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    customer_email = models.EmailField(verbose_name="Эл.Почта")
    order_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата")
    status = models.CharField(max_length=50, choices=PaymentStatus.choices, verbose_name="Статус")
    paid = models.BooleanField(default=False)
    start_date = models.DateField(verbose_name="Дата начала", null=True)
    end_date = models.DateField(verbose_name="Дата окончания", blank=True, null=True)

    class Meta:
        verbose_name_plural = "Бронирования"
        verbose_name = "Бронирование"



    def __str__(self):
        return f"Order {self.id} for {self.customer_user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    jew = models.ForeignKey(Jewelry, on_delete=models.CASCADE)
    quantity = models.IntegerField(verbose_name="Кол-во людей")

    def __str__(self):
        return f"{self.quantity} of {self.jew} for {self.order}"
