import json

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate

from core.authors.tests.util import setupUser
from core.posts.models import Posts
from core.posts.views import PostsViewSet


class PostViewsTest(TestCase):

    def setUp(self):
        self.author1 = setupUser("cry")
        self.factory = APIRequestFactory()

    def test_create_post(self):
        author_id = str(self.author1.id)
        data = {
            "author": author_id,
            "title": "wild",
            "source": "http://www.chaitali.com/",
            "origin": "http://www.cry.com/",
            "visibleTo": ["whomever"],
            "unlisted": True,
            "visibility": "PRIVATE",
            "categories": ["cool", "fun", "sad"]
        }
        post_data = json.dumps(data)
        response = self.client.post('/posts/', {'query': 'createpost', 'postData': post_data})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["query"], "createpost")
        self.assertEqual(response.data["message"], "Post created")

    # From https://stackoverflow.com/questions/11170425/how-to-unit-test-file-upload-in-django, credits to Danilo Cabello
    def test_valid_file_type(self):
        author_id = str(self.author1.id)
        data = {
            "author": author_id,
            "title": "wild"
        }
        post_data = json.dumps(data)
        fp = SimpleUploadedFile("file.jpg", b"file_content", content_type="image/jpeg")
        response = self.client.post('/posts/', {'imageFiles': fp, 'query': 'createpost', 'postData': post_data})
        self.assertEqual(response.status_code, 200)

    def test_invalid_file_type(self):
        author_id = str(self.author1.id)
        data = {
            "author": author_id,
            "title": "wild"
        }
        post_data = json.dumps(data)
        fp = SimpleUploadedFile("file.mp4", b"file_content", content_type="video/mp4")
        response = self.client.post('/posts/', {'imageFiles': fp, 'query': 'createpost', 'postData': post_data})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["message"], "Invalid file type")

    def test_multiple_files(self):
        author_id = str(self.author1.id)
        data = {
            "author": author_id,
            "title": "wild"
        }
        post_data = json.dumps(data)
        fp = SimpleUploadedFile("file.jpg", b"file_content", content_type="image/jpeg")
        fp2 = SimpleUploadedFile("file2.jpg", b"file_content", content_type="image/png")
        response = self.client.post('/posts/', {'imageFiles': {fp, fp2}, 'query': 'createpost', 'postData': post_data})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(Posts.objects.filter(author=author_id)), 3)

    def test_delete_post(self):
        author_id = str(self.author1.id)
        data = {
            "author": author_id,
            "title": "wild"
        }
        post_data = json.dumps(data)
        response = self.client.post('/posts/', {'query': 'createpost', 'postData': post_data})

        post = Posts.objects.get(author=author_id)
        response = self.client.delete(f'/posts/{post.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["message"], "Post deleted successfully")
        self.assertEqual(len(Posts.objects.filter(id=post.id)), 0)

    def test_list_posts_unauthenticated(self):
        author_id = str(self.author1.id)
        data = {
            "author": author_id,
            "title": "wild"
        }
        post_data = json.dumps(data)
        fp = SimpleUploadedFile("file.jpg", b"file_content", content_type="image/jpeg")
        response = self.client.post('/posts/', {'imageFiles': fp, 'query': 'createpost', 'postData': post_data})
        self.assertEqual(response.status_code, 200)

        view = PostsViewSet.as_view({'get': 'list'})
        request = self.factory.get(reverse('posts-list'))
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.data)
        for post in response.data['results']:
            print(post['contentType'])
            self.assertNotIn("image", post['contentType'])

    def test_list_posts_authenticated(self):
        author_id = str(self.author1.id)
        data = {
            "author": author_id,
            "title": "wild"
        }
        post_data = json.dumps(data)
        fp = SimpleUploadedFile("file.jpg", b"file_content", content_type="image/jpeg")
        response = self.client.post('/posts/', {'imageFiles': fp, 'query': 'createpost', 'postData': post_data})
        self.assertEqual(response.status_code, 200)

        view = PostsViewSet.as_view({'get': 'list'})
        request = self.factory.get(reverse('posts-list'))
        force_authenticate(request, user=get_user_model().objects.get(username="cry"))
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.data)
        for post in response.data['results']:
            if 'text' in post['contentType']:
                continue
            self.assertIn("image", post['contentType'])
