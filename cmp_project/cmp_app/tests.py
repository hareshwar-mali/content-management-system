from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import User

class UserTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.url = reverse('user-list')

    def test_create_user(self):
        data = {
            'email': 'author@example.com',
            'password': 'TestPassword123',
            'first_name': 'John',
            'last_name': 'Doe',
            'phone': '1234567890',
            'pincode': '123456',
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
