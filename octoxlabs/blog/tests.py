from django.test import TestCase
from django.urls import reverse
from blog.serializers import PostSerializer
from django.contrib.auth import get_user_model
from .models import Post, Tag
from unittest.mock import patch, MagicMock

from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()


class PostAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)
        post = Post.objects.create(title='Test Post', content='Test Content', author=self.user)
        self.post_id = post.id
        self.post = post
        self.valid_data = {
            "title": "Test Title",
            "content": "Test Content"
        }
        self.invalid_data = {
            "title": "",
            "content": "Content with no title"
        }
    
    @patch('redis.Redis')
    def test_create_post(self, mock_redis):
        mock_redis_instance = MagicMock()
        mock_redis.return_value = mock_redis_instance
        response = self.client.post(reverse('posts'), {'title': 'New Post', 'content': 'Post content'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        mock_redis_instance.rpush.assert_called_once()


    def test_get_post_list(self):
        response = self.client.get(reverse('post_list'))
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_get_single_post(self):
        url = reverse('post_detail', kwargs={'post_id': self.post_id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['title'], 'Test Post')
    
    @patch('redis.Redis') 
    def test_update_post_with_valid_data(self, mock_redis):
        mock_redis_instance = MagicMock()
        mock_redis.return_value = mock_redis_instance
        url = reverse('post_detail', kwargs={'post_id': self.post_id})
        response = self.client.put(url, data=self.valid_data)
        self.post.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.post.title, self.valid_data['title'])
        self.assertEqual(self.post.content, self.valid_data['content'])
        mock_redis_instance.rpush.assert_called_once()

    @patch('redis.Redis') 
    def test_delete_post(self, mock_redis):
        mock_redis_instance = MagicMock()
        mock_redis.return_value = mock_redis_instance
        url = reverse('post_detail', kwargs={'post_id': self.post_id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Post.objects.filter(id=self.post_id).exists())
        mock_redis_instance.rpush.assert_called_once()


