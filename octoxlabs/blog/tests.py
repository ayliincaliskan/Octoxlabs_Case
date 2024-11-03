from django.test import TestCase
from django.urls import reverse
from blog.serializers import PostSerializer
from .models import Post, Tag
from unittest.mock import patch, MagicMock

from rest_framework import status
from rest_framework.test import APITestCase


class TagModelTest(TestCase):
    def setUp(self):
        self.tag = Tag.objects.create(name='Test Tag')

    def test_tag_creation(self):
        self.assertEqual(self.tag.name, 'Test Tag')


class PostModelTests(TestCase):
    def setUp(self):
        self.post = Post.objects.create(title="Test Post", content="This is a test content.")
        self.post_id = self.post.id
        self.valid_data = {
            "title": "Test Title",
            "content": "Test Content"
        }
        self.invalid_data = {
            "title": "",
            "content": "Content with no title"
        }

    def test_post_creation(self):
        self.assertEqual(self.post.title, 'Test Post')
        self.assertEqual(self.post.content, 'This is a test content.')

    def test_post_str(self):
        self.assertEqual(str(self.post.title), 'Test Post')


class PostAPITests(APITestCase):
    def setUp(self):
        post = Post.objects.create(title='Test Post', content='Test Content')
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


class TagAPITests(APITestCase):
    def setUp(self):
        self.tag = Tag.objects.create(name='Test Tag')
        self.tag_id = self.tag.id
        self.url = reverse('tag_detail', kwargs={'tag_id': self.tag_id})

    def test_get_single_tag(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['name'], self.tag.name)
    
    @patch('redis.Redis') 
    def test_post_tag(self, mock_redis):
        mock_redis_instance = MagicMock()
        mock_redis.return_value = mock_redis_instance
        response = self.client.post(reverse('tags'), {'name': 'New Tag'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Tag.objects.count(), 2)
        mock_redis_instance.rpush.assert_called_once()

    @patch('redis.Redis') 
    def test_put_tag(self, mock_redis):
        mock_redis_instance = MagicMock()
        mock_redis.return_value = mock_redis_instance
        response = self.client.put(self.url, {'name': 'Updated Tag'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.tag.refresh_from_db()
        self.assertEqual(self.tag.name, 'Updated Tag')
        mock_redis_instance.rpush.assert_called_once()

    @patch('redis.Redis') 
    def test_delete_tag(self, mock_redis):
        mock_redis_instance = MagicMock()
        mock_redis.return_value = mock_redis_instance
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Tag.objects.count(), 0)
        mock_redis_instance.rpush.assert_called_once()

    def test_delete_non_existent_tag(self):
        response = self.client.delete(reverse('tag_detail', kwargs={'tag_id': 999}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)