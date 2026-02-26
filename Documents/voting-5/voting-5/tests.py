from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse

from .models import Poll, Choice, Vote
from .forms import VoteForm

"""Тесты моделей опроса и голосования."""

class PollModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user('testuser', 'test@test.com', 'pass')
        self.poll = Poll.objects.create(question='Тестовый вопрос?', created_by=self.user)
        self.choice1 = Choice.objects.create(poll=self.poll, text='Вариант 1')
        self.choice2 = Choice.objects.create(poll=self.poll, text='Вариант 2')
        
"""Создание опроса и вариантов ответа."""

    def test_poll_creation(self):
        
        self.assertEqual(self.poll.question, 'Тестовый вопрос?')
        self.assertEqual(self.poll.created_by, self.user)
        self.assertEqual(self.poll.choices.count(), 2)

"""Тесты логики голосования."""


class VotingLogicTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user('voter', 'v@v.com', 'pass')
        self.poll = Poll.objects.create(question='Голосуем?', created_by=self.user)
        self.choice_a = Choice.objects.create(poll=self.poll, text='A')
        self.choice_b = Choice.objects.create(poll=self.poll, text='B')
        
"""Результаты: сумма голосов по вариантам равна общему числу голосов."""

    def test_results_calculation(self):
        Vote.objects.create(poll=self.poll, choice=self.choice_a, user=self.user)
        u2 = User.objects.create_user('voter2', 'v2@v.com', 'pass')
        Vote.objects.create(poll=self.poll, choice=self.choice_b, user=u2)
        total = self.poll.get_total_votes()
        sum_choices = sum(c.get_votes_count() for c in self.poll.choices.all())
        self.assertEqual(total, 2)
        self.assertEqual(sum_choices, 2)

"""Тесты создания опросов через представление."""


class PollCreationTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user('creator', 'c@c.com', 'pass')
        self.client = Client()
        self.client.login(username='creator', password='pass')
        
"""Создание опроса доступно только авторизованным."""
        

    def test_poll_create_view_requires_login(self):
        self.client.logout()
        url = reverse('app:poll_create')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 302)
        self.assertIn('login', resp.url)
        
"""POST на создание опроса создаёт опрос и редиректит на список."""
        

    def test_poll_create_view_post_creates_poll(self):
        url = reverse('app:poll_create')
        resp = self.client.post(url, {
            'question': 'Опрос с формы',
            'choice1': 'Один',
            'choice2': 'Два',
            'choice3': 'Три',
        })
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.url, reverse('app:poll_list'))
        self.assertEqual(Poll.objects.count(), 1)
        poll = Poll.objects.get(question='Опрос с формы')
        self.assertEqual(poll.choices.count(), 3)
        
"""Тесты главной страницы и голосования."""


class PollListAndVoteTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user('u', 'u@u.com', 'pass')
        self.poll = Poll.objects.create(question='Список и голос?', created_by=self.user)
        Choice.objects.create(poll=self.poll, text='Да')
        Choice.objects.create(poll=self.poll, text='Нет')
        self.client = Client()
        
"""На главной показывается форма голосования, если пользователь не голосовал."""

    def test_list_shows_vote_form_when_not_voted(self):
        resp = self.client.get(reverse('app:poll_list'))
        self.assertEqual(resp.status_code, 200)
        item = next(i for i in resp.context['poll_list_data'] if i['poll'] == self.poll)
        self.assertFalse(item['voted'])
        self.assertIn('form', item)
        self.assertIsInstance(item['form'], VoteForm)
        
"""После отправки голоса с главной — редирект на главную, голос учтён."""

    def test_vote_submit_redirects_to_list(self):
        url = reverse('app:vote_submit', kwargs={'pk': self.poll.pk})
        choice = self.poll.choices.first()
        resp = self.client.post(url, {'choice': choice.pk})
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.url, reverse('app:poll_list'))
        self.assertEqual(self.poll.get_total_votes(), 1)
