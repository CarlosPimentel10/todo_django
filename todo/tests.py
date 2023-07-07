from django.test import TestCase
from django.urls import reverse
from todo.models import Task
from django.utils import timezone

class TestHomeView(TestCase):
    def setUp(self):
        self.url = reverse('home')
        
        # Create test tasks
        self.task1 = Task.objects.create(task='Task1', is_completed=False, updated_at=timezone.now())
        self.task2 = Task.objects.create(task='Task2', is_completed=True, updated_at=timezone.now())
        self.task3 = Task.objects.create(task='Task3', is_completed=False, updated_at=timezone.now())

    def test_home_view(self):
        response = self.client.get(self.url)

        # Assert the response status code
        self.assertEqual(response.status_code, 200)

        # Assert that the correct template is used
        self.assertTemplateUsed(response, 'home.html')

        # Assert that the response contains the tasks
        self.assertIn('tasks', response.context)
        self.assertIn(self.task1, response.context['tasks'])
        self.assertIn(self.task3, response.context['tasks'])

        # Assert that the response contains the completed task
        self.assertIn('task_completed', response.context)
        self.assertIn(self.task2, response.context['task_completed'])

        # Assert the order of tasks and completed tasks
        tasks = response.context['tasks']
        task_completed = response.context['task_completed']
        self.assertEqual(list(tasks), [self.task3, self.task1])
        self.assertEqual(list(task_completed), [self.task2])
