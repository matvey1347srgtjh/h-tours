from django.db import models

class Task(models.Model):

    class Status(models.TextChoices):
        TODO = 'todo', 'Нужно сделать'
        IN_PROGRESS = 'progress', 'В процессе'
        DONE = 'done', 'Завершено'

    title = models.CharField(max_length=100, verbose_name='Название задачи')
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.TODO, verbose_name='статус')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'