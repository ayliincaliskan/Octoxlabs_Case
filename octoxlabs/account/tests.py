from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from core.utils import messages
from unittest.mock import patch, MagicMock

User = get_user_model()


class UserAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.user_id = self.user.id
        self.url = reverse('user_detail', kwargs={'id': self.user_id})

    @patch('redis.Redis')
    def test_create_user(self, mock_redis):
        mock_redis_instance = MagicMock()
        mock_redis.return_value = mock_redis_instance
        response = self.client.post(reverse('user_create'), {
            'username': 'newuser',
            'password': 'newpassword123',
            'email': 'newuser@example.com'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(response.data['message'], messages['USER_CREATE'])

        mock_redis_instance.rpush.assert_called_once()

    def test_retrieve_user(self):
        self.client.force_authenticate(user=self.user) 
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], self.user.username)

    @patch('redis.Redis')
    def test_delete_user(self, mock_redis):
        mock_redis_instance = MagicMock()
        mock_redis.return_value = mock_redis_instance
        self.client.force_authenticate(user=self.user) 
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(User.objects.count(), 0)
        mock_redis_instance.rpush.assert_called_once()

    def test_list_users(self):
        self.client.force_authenticate(user=self.user) 
        response = self.client.get(reverse('user_list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_user_without_password(self):
        self.client.force_authenticate(user=self.user) 
        response = self.client.post(reverse('user_create'), {
            'username': 'newuser',
            'email': 'newuser@example.com'
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)  
