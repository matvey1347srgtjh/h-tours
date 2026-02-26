from django.db import models
from django.utils import timezone


class Post(models.Model):
    author_name = models.CharField(max_length=40, verbose_name="Автор поста")
    title = models.CharField(max_length=255, verbose_name="Название поста")
    text = models.TextField(verbose_name="Текст поста")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Дата создания")

    class Meta:
        pass

    def __str__(self):
        return f"{self.title} (от {self.author_name})"
    

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name="Пост")
    author = models.CharField(max_length=100, verbose_name="Имя коментатора")
    text_comment = models.TextField(max_length=255, verbose_name="Текст коментария")
    created_date = models.DateTimeField(default=timezone.now, verbose_name="Дата коментария")

    class Meta:
        pass

    def __str__(self):
        return f"Коментарий от {self.author} к посту {self.post.id}"
