from django.test import TestCase, Client
from django.urls import reverse
from .models import Task
from todo.forms import TaskForm


class TaskModelTest(TestCase):
    
    def test_task_creation(self):
        task = Task.objects.create(title="Тестовая задача")
        
        self.assertEqual(task.title, "Тестовая задача")
        self.assertEqual(task.status, Task.Status.TODO)
        self.assertIsNotNone(task.created_at)
        self.assertEqual(str(task), "Тестовая задача")


class TaskCollectionTest(TestCase):
    
    def setUp(self):
        self.task1 = Task.objects.create(title="Первая задача", status=Task.Status.TODO)
        self.task2 = Task.objects.create(title="Вторая задача", status=Task.Status.IN_PROGRESS)
        self.task3 = Task.objects.create(title="Третья задача", status=Task.Status.DONE)
    
    def test_task_list_ordering(self):
        tasks = Task.objects.all().order_by('-created_at')
        tasks_list = list(tasks)
        
        self.assertEqual(len(tasks_list), 3)
        self.assertEqual(tasks_list[0].title, "Третья задача")
        self.assertEqual(tasks_list[1].title, "Вторая задача")
        self.assertEqual(tasks_list[2].title, "Первая задача")
    
    def test_task_filtering_by_status(self):
        todo_tasks = Task.objects.filter(status=Task.Status.TODO)
        progress_tasks = Task.objects.filter(status=Task.Status.IN_PROGRESS)
        done_tasks = Task.objects.filter(status=Task.Status.DONE)
        
        self.assertEqual(todo_tasks.count(), 1)
        self.assertEqual(progress_tasks.count(), 1)
        self.assertEqual(done_tasks.count(), 1)
        
        self.assertIn(self.task1, todo_tasks)
        self.assertIn(self.task2, progress_tasks)
        self.assertIn(self.task3, done_tasks)


class TaskStatusToggleTest(TestCase):
    
    def test_status_toggle_cycle(self):
        task = Task.objects.create(title="Тестовая задача", status=Task.Status.TODO)
        order = [Task.Status.TODO, Task.Status.IN_PROGRESS, Task.Status.DONE]
        
        current_index = order.index(task.status)
        next_index = (current_index + 1) % len(order)
        task.status = order[next_index]
        task.save()
        self.assertEqual(task.status, Task.Status.IN_PROGRESS)
        
        current_index = order.index(task.status)
        next_index = (current_index + 1) % len(order)
        task.status = order[next_index]
        task.save()
        self.assertEqual(task.status, Task.Status.DONE)
        
        current_index = order.index(task.status)
        next_index = (current_index + 1) % len(order)
        task.status = order[next_index]
        task.save()
        self.assertEqual(task.status, Task.Status.TODO)


class TaskFormTest(TestCase):
    
    def test_form_valid_data(self):
        form_data = {
            'title': 'Новая задача',
            'status': Task.Status.TODO
        }
        form = TaskForm(data=form_data)
        
        self.assertTrue(form.is_valid())
        task = form.save()
        self.assertEqual(task.title, 'Новая задача')
        self.assertEqual(task.status, Task.Status.TODO)


class TaskViewsTest(TestCase):
    
    def setUp(self):
        self.client = Client()
        self.task = Task.objects.create(title="Тестовая задача", status=Task.Status.TODO)
    
    def test_task_create_view_post(self):
        form_data = {
            'title': 'Новая задача через форму',
            'status': Task.Status.IN_PROGRESS
        }
        response = self.client.post(reverse('task_create'), data=form_data)
        
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Task.objects.filter(title='Новая задача через форму').exists())
