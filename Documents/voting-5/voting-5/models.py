from django.db import models
from django.contrib.auth.models import User


class Poll(models.Model):
    question = models.CharField('Вопрос', max_length=255)
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='created_polls',
        null=True,
        blank=True
    )
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)

    class Meta:
        verbose_name = 'Опрос'
        verbose_name_plural = 'Опросы'
        ordering = ['-created_at']

    def __str__(self):
        return self.question

    def get_total_votes(self):
        return Vote.objects.filter(poll=self).count()


class Choice(models.Model):
    poll = models.ForeignKey(
        Poll,
        on_delete=models.CASCADE,
        related_name='choices',
        verbose_name='Опрос'
    )
    text = models.CharField('Текст варианта', max_length=255)

    class Meta:
        verbose_name = 'Вариант ответа'
        verbose_name_plural = 'Варианты ответов'

    def __str__(self):
        return self.text

    def get_votes_count(self):
        return self.votes.count()


class Vote(models.Model):
    poll = models.ForeignKey(
        Poll,
        on_delete=models.CASCADE,
        related_name='votes',
        verbose_name='Опрос'
    )
    choice = models.ForeignKey(
        Choice,
        on_delete=models.CASCADE,
        related_name='votes',
        verbose_name='Вариант'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='votes',
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = 'Голос'
        verbose_name_plural = 'Голоса'
        constraints = [
            models.UniqueConstraint(
                fields=['poll', 'user'],
                condition=models.Q(user__isnull=False),
                name='unique_user_vote_per_poll'
            )
        ]

    def __str__(self):
        return f'{self.poll}: {self.choice}'
