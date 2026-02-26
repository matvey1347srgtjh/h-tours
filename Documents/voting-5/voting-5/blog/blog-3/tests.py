from django.test import TestCase, Client
from django.urls import reverse
from .models import Post, Comment

class BlogTests(TestCase):
    def setUp(self):
        # создаем тестовый пост
        self.client = Client()
        self.post = Post.objects.create(
            title="Тестовый заголовок",
            text="Тестовый текст поста",
            author_name="Тестер"
        )

    # --- Тесты Постов --- #

    def test_post_creation(self):
        """Проверка создания поста"""
        response = self.client.post(reverse('post-new'), {
            'title': 'Новый пост через тест',
            'text': 'Содержание нового поста',
            'author_name': 'Админ'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Post.objects.filter(title='Новый пост через тест').exists())

    def test_post_edit(self):
        """Проверка редактирования поста"""
        response = self.client.post(reverse('post-edit', kwargs={'pk': self.post.pk}), {
            'title': 'Измененный заголовок',
            'text': 'Измененный текст',
            'author_name': 'Тестер'
        })
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, 'Измененный заголовок')

    def test_post_delete(self):
        """Проверка удаления поста"""
        response = self.client.post(reverse('post-delete', kwargs={'pk': self.post.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Post.objects.count(), 0)

    # --- Тесты Комментариев --- #

    def test_comment_creation(self):
        """Проверка создания комментария к посту"""
        # Имитируем post запрос на страницу списка где лежит форма комента
        response = self.client.post(reverse('blog-list'), {
            'post_id': self.post.id,
            'author': 'Иван',
            'text_comment': 'Крутой пост!'
        })
        self.assertEqual(Comment.objects.count(), 1)
        comment = Comment.objects.first()
        self.assertEqual(comment.text_comment, 'Крутой пост!')
        self.assertEqual(comment.post, self.post)

    # --- Тесты отображения --- #

    def test_blog_list_view(self):
        """Проверка доступности главной страницы"""
        response = self.client.get(reverse('blog-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Тестовый заголовок")