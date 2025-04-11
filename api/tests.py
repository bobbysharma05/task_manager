from django.test import TestCase

# Create your tests here.
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Task

class UserTests(APITestCase):
    def test_create_user(self):
        """
        Ensure we can create a new user.
        """
        url = reverse('register')
        data = {'username': 'testuser', 'email': 'test@example.com', 'password': 'testpassword123'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'testuser')
    
    def test_login_user(self):
        """
        Ensure we can login and receive a token.
        """
        # Create a user first
        User.objects.create_user(username='testuser', password='testpassword123')
        
        url = reverse('token_obtain_pair')
        data = {'username': 'testuser', 'password': 'testpassword123'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('access' in response.data)

class TaskTests(APITestCase):
    def setUp(self):
        # Create a user and get token
        self.user = User.objects.create_user(username='testuser', password='testpassword123')
        url = reverse('token_obtain_pair')
        data = {'username': 'testuser', 'password': 'testpassword123'}
        response = self.client.post(url, data, format='json')
        self.token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
    
    def test_create_task(self):
        """
        Ensure we can create a new task.
        """
        url = reverse('task-list-create')
        data = {'title': 'Test Task', 'description': 'Test Description', 'status': 'TODO'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 1)
        self.assertEqual(Task.objects.get().title, 'Test Task')
        self.assertEqual(Task.objects.get().owner, self.user)
    
    def test_list_tasks(self):
        """
        Ensure we can list tasks.
        """
        # Create a task first
        Task.objects.create(title='Test Task', owner=self.user)
        
        url = reverse('task-list-create')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
    
    def test_retrieve_task(self):
        """
        Ensure we can retrieve a task.
        """
        task = Task.objects.create(title='Test Task', owner=self.user)
        
        url = reverse('task-detail', kwargs={'pk': task.id})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Task')
    
    def test_update_task(self):
        """
        Ensure we can update a task.
        """
        task = Task.objects.create(title='Test Task', owner=self.user)
        
        url = reverse('task-detail', kwargs={'pk': task.id})
        data = {'title': 'Updated Task', 'status': 'IN_PROGRESS'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        task.refresh_from_db()
        self.assertEqual(task.title, 'Updated Task')
        self.assertEqual(task.status, 'IN_PROGRESS')
    
    def test_delete_task(self):
        """
        Ensure we can delete a task.
        """
        task = Task.objects.create(title='Test Task', owner=self.user)
        
        url = reverse('task-detail', kwargs={'pk': task.id})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.count(), 0)
    
    def test_other_user_cannot_access_task(self):
        """
        Ensure other users cannot access tasks they don't own.
        """
        task = Task.objects.create(title='Test Task', owner=self.user)
        
        # Create another user and authenticate as them
        other_user = User.objects.create_user(username='otheruser', password='testpassword123')
        url = reverse('token_obtain_pair')
        data = {'username': 'otheruser', 'password': 'testpassword123'}
        response = self.client.post(url, data, format='json')
        self.token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        
        # Try to access the first user's task
        url = reverse('task-detail', kwargs={'pk': task.id})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)