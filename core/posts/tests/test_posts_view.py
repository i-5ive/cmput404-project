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
        self.author1 = setupUser("cry", "password")
        self.author2 = setupUser("user2", "password")
        self.factory = APIRequestFactory()
        
        self.client.login(username="cry", password="password")

    def test_create_post_wrong_user_authentication(self):
        self.client.login(username="user2", password="password")
        author_id = str(self.author1.id)
        data = {
            "author": author_id,
            "title": "wild",
            "unlisted": True,
            "visibility": "PRIVATE",
            "categories": ["cool", "fun", "sad"]
        }
        post_data = json.dumps(data)
        response = self.client.post('/posts/', {'query': 'createpost', 'postData': post_data})
        self.assertEqual(response.status_code, 401)
        
    def test_create_post_unauthenticated(self):
        self.client.logout()
        author_id = str(self.author1.id)
        data = {
            "author": author_id,
            "title": "wild",
            "unlisted": True,
            "visibility": "PRIVATE",
            "categories": ["cool", "fun", "sad"]
        }
        post_data = json.dumps(data)
        response = self.client.post('/posts/', {'query': 'createpost', 'postData': post_data})
        self.assertEqual(response.status_code, 401)
        
    def test_unfound_users(self):
        author_id = str(self.author1.id)
        data = {
            "author": author_id,
            "title": "wild",
            "unlisted": True,
            "visibility": "PRIVATE",
            "categories": ["cool", "fun", "sad"]
        }
        post_data = json.dumps(data)
        response = self.client.post('/posts/', {'query': 'createpost', 'postData': post_data, 'visibleTo': json.dumps(["a", "b"])})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(sorted(response.data["invalidUsers"]), ["a", "b"])
    
    def test_one_unfound_user(self):
        author_id = str(self.author1.id)
        data = {
            "author": author_id,
            "title": "wild",
            "unlisted": True,
            "visibility": "PRIVATE",
            "categories": ["cool", "fun", "sad"]
        }
        post_data = json.dumps(data)
        response = self.client.post('/posts/', {'query': 'createpost', 'postData': post_data, 'visibleTo': json.dumps(["b"])})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(sorted(response.data["invalidUsers"]), ["b"])
    
    def test_all_valid_users(self):
        author_id = str(self.author1.id)
        data = {
            "author": author_id,
            "title": "wild",
            "unlisted": True,
            "visibility": "PRIVATE",
            "categories": ["cool", "fun", "sad"]
        }
        post_data = json.dumps(data)
        response = self.client.post('/posts/', {'query': 'createpost', 'postData': post_data, 'visibleTo': json.dumps(["cry", "user2"])})
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(response.data.get("invalidUsers"))

        posts = Posts.objects.all()
        self.assertEqual(len(posts), 1)
        self.assertEqual(sorted(posts.first().visibleTo), sorted([self.author1.get_url(), self.author2.get_url()]))
    
    def test_create_private_add_author(self):
        author_id = str(self.author1.id)
        data = {
            "author": author_id,
            "title": "wild",
            "unlisted": True,
            "visibility": "PRIVATE",
            "categories": ["cool", "fun", "sad"]
        }
        post_data = json.dumps(data)
        response = self.client.post('/posts/', {'query': 'createpost', 'postData': post_data, 'visibleTo': json.dumps(["user2"])})
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(response.data.get("invalidUsers"))

        posts = Posts.objects.all()
        self.assertEqual(len(posts), 1)
        self.assertEqual(sorted(posts.first().visibleTo), sorted([self.author1.get_url(), self.author2.get_url()]))
    
    def test_create_post_public_no_visible_to(self):
        author_id = str(self.author1.id)
        data = {
            "author": author_id,
            "title": "wild",
            "unlisted": True,
            "visibility": "PUBLIC",
            "categories": ["cool", "fun", "sad"]
        }
        post_data = json.dumps(data)
        response = self.client.post('/posts/', {'query': 'createpost', 'postData': post_data})
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(response.data.get("invalidUsers"))

        posts = Posts.objects.all()
        self.assertEqual(len(posts), 1)
        self.assertEqual(len(posts.first().visibleTo), 0)
    
    
    def test_create_post(self):
        author_id = str(self.author1.id)
        data = {
            "author": author_id,
            "title": "wild",
            "unlisted": True,
            "visibility": "PRIVATE",
            "categories": ["cool", "fun", "sad"]
        }
        post_data = json.dumps(data)
        response = self.client.post('/posts/', {'query': 'createpost', 'postData': post_data})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["query"], "createpost")
        self.assertEqual(response.data["message"], "Post created")
        
        posts = Posts.objects.all()
        self.assertEqual(len(posts), 1)
        self.assertEqual(len(posts.first().visibleTo), 0)

    # From https://stackoverflow.com/a/27345260, credits to Danilo Cabello
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

    def test_application_base64_file(self):
        author_id = str(self.author1.id)
        data = {
            "author": author_id,
            "title": "wild"
        }
        post_data = json.dumps(data)
        fp = SimpleUploadedFile("app.dat", b"file_content", content_type="application/base64")
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
        response = self.client.delete('/posts/{0}/'.format(post.id))
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
        for post in response.data['posts']:
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
        for post in response.data['posts']:
            if 'text' in post['contentType']:
                continue
            self.assertIn("image", post['contentType'])

    def test_list_posts_unlisted(self):
        author_id = str(self.author1.id)
        data = {
            "author": author_id,
            "title": "wild",
            "unlisted": True
        }
        post_data = json.dumps(data)
        response = self.client.post('/posts/', {'query': 'createpost', 'postData': post_data})
        self.assertEqual(response.status_code, 200)

        view = PostsViewSet.as_view({'get': 'list'})
        request = self.factory.get(reverse('posts-list'))
        force_authenticate(request, user=get_user_model().objects.get(username="cry"))
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["posts"]), 0)
        self.assertEqual(len(Posts.objects.all()), 1)

    def test_deletion_unauthenticated(self):
        self.client.logout()
        post = Posts.objects.create(author=self.author1)
        res = self.client.delete("/posts/{0}/".format(post.id))
        self.assertEqual(res.status_code, 401)
        self.assertEqual(len(Posts.objects.all()), 1)
        
    def test_deletion_wrong_user_authentication(self):
        self.client.login(username="user2", password="password")
        post = Posts.objects.create(author=self.author1)
        res = self.client.delete("/posts/{0}/".format(post.id))
        self.assertEqual(res.status_code, 401)
        self.assertEqual(len(Posts.objects.all()), 1)
