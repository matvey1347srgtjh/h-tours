from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg


# Create your models here.

class Jewelry(models.Model):
    name = models.TextField(max_length=100, verbose_name="Название")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    image = models.ImageField(upload_to='images/', verbose_name="Фото")
    description = models.TextField(blank=True, null=True, verbose_name="Описание") 
    days = models.IntegerField(default=0, verbose_name="Кол-во дней")  
    city = models.CharField(max_length=50, default=0, verbose_name="Город")
    
    class Meta:
        verbose_name = "Тур"
        verbose_name_plural = "Туры"

    def __str__(self):
        return self.name
    
    def average_rating(self):
        from order.models import OrderItem
        order_items = OrderItem.objects.filter(jew=self)
        reviews = Review.objects.filter(order__in=[item.order for item in order_items])
        return reviews.aggregate(Avg('rating'))['rating__avg'] or 0
    
class Favorite(models.Model):
       user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
       jewelry = models.ForeignKey(Jewelry, on_delete=models.CASCADE, verbose_name="Тур")

       class Meta:
           unique_together = ('user', 'jewelry')
           verbose_name = "Избранное"
           verbose_name_plural = "Избранное"
       def __str__(self):
           return f"{self.user.username} - {self.jewelry.name}"
       


class Slide(models.Model):
    title = models.CharField(max_length=200, verbose_name = "Заголовок")
    description = models.TextField(verbose_name = "Описание")

    class Meta:
        verbose_name = "Слайд"
        verbose_name_plural = "Слайды"

    def __str__(self):
        return self.title
    
    
from django.db import models
from django.contrib.auth.models import User
from order.models import Order

class Review(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='review', verbose_name="Бронь")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)], verbose_name="Рейтинг")
    comment = models.TextField(verbose_name="Комментарий")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name="Отзыв"
        verbose_name_plural = "Отзывы"

    def __str__(self):
        return f"Review by {self.user.username} for Order {self.order.id}"