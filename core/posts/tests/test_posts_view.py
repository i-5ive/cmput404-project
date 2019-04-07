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
        self.assertEqual(response.status_code, 403)
        self.assertEqual(Posts.objects.all().count(), 0)
        
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
        self.assertEqual(response.status_code, 403)
        self.assertEqual(Posts.objects.all().count(), 0)
        
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
        self.assertEqual(Posts.objects.all().count(), 0)
    
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
        self.assertEqual(Posts.objects.all().count(), 0)
    
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
        self.assertEqual(posts.first().visibility, "PRIVATE")
        self.assertEqual(posts.first().title, "wild")
        self.assertEqual(posts.first().categories, ["cool", "fun", "sad"])
        self.assertTrue(posts.first().unlisted)
        self.assertEqual(sorted(posts.first().visibleTo), sorted([self.author1.get_url(), self.author2.get_url()]))
    
    def test_all_valid_users_external(self):
        author_id = str(self.author1.id)
        data = {
            "author": author_id,
            "title": "wild",
            "unlisted": True,
            "visibility": "PRIVATE",
            "categories": ["cool", "fun", "sad"]
        }
        post_data = json.dumps(data)
        response = self.client.post('/posts/', {'query': 'createpost', 'postData': post_data, 'visibleTo': json.dumps(["cry", "user2", "https://somevaliduser.awekawieawe/author/25"])})
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(response.data.get("invalidUsers"))

        posts = Posts.objects.all()
        self.assertEqual(len(posts), 1)
        self.assertEqual(posts.first().visibility, "PRIVATE")
        self.assertEqual(posts.first().title, "wild")
        self.assertEqual(posts.first().categories, ["cool", "fun", "sad"])
        self.assertTrue(posts.first().unlisted)
        self.assertEqual(sorted(posts.first().visibleTo), sorted([self.author1.get_url(), self.author2.get_url(), "https://somevaliduser.awekawieawe/author/25"]))
    
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
        self.assertEqual(posts.first().visibility, "PRIVATE")
        self.assertEqual(posts.first().title, "wild")
        self.assertEqual(posts.first().categories, ["cool", "fun", "sad"])
        self.assertTrue(posts.first().unlisted)
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
        self.assertEqual(posts.first().visibility, "PUBLIC")
        self.assertEqual(posts.first().title, "wild")
        self.assertEqual(posts.first().categories, ["cool", "fun", "sad"])
        self.assertTrue(posts.first().unlisted)
        self.assertEqual(len(posts.first().visibleTo), 0)
    
    def test_create_post(self):
        author_id = str(self.author1.id)
        data = {
            "author": author_id,
            "title": "wild",
            "unlisted": True,
            "visibility": "PRIVATE",
            "categories": ["cool", "fun", "sad"],
            "description": "A description about the post",
            "content": "!! POST CONTENT !! [imgTag](https://somefakeimage11111111111.core)"
        }
        post_data = json.dumps(data)
        response = self.client.post('/posts/', {'query': 'createpost', 'postData': post_data})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["query"], "createpost")
        self.assertEqual(response.data["message"], "Post created")
        
        posts = Posts.objects.all()
        self.assertEqual(len(posts), 1)
        self.assertEqual(len(posts.first().visibleTo), 0)

        post = posts[0]
        self.assertEqual(post.author, self.author1)
        self.assertEqual(post.title, data["title"])
        self.assertEqual(post.unlisted, data["unlisted"])
        self.assertEqual(post.visibility, data["visibility"])
        self.assertEqual(post.categories, data["categories"])
        self.assertEqual(post.description, data["description"])
        self.assertEqual(post.content, data["content"])
        self.assertEqual(post.contentType, "text/markdown")
        self.assertEqual(post.comments.count(), 0)

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
        self.assertTrue(Posts.objects.all().count(), 2)
        
        text_posts = Posts.objects.filter(contentType="text/markdown")
        text_post = text_posts.first()
        self.assertEqual(len(text_posts), 1)
        self.assertEqual(text_post.author, self.author1)
        self.assertEqual(text_post.title, "wild")

        image_posts = Posts.objects.filter(post_id=text_post.post_id, contentType="image/jpeg;base64")
        self.assertEqual(len(image_posts), 1)
        self.assertEqual(image_posts.first().content, "image/jpeg;base64,ZmlsZV9jb250ZW50")

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
        self.assertTrue(Posts.objects.all().count(), 2)
        
        text_posts = Posts.objects.filter(contentType="text/markdown")
        text_post = text_posts.first()
        self.assertEqual(len(text_posts), 1)
        self.assertEqual(text_post.author, self.author1)
        self.assertEqual(text_post.title, "wild")

        data_posts = Posts.objects.filter(post_id=text_post.post_id, contentType="application/base64")
        self.assertEqual(len(data_posts), 1)
        self.assertEqual(data_posts.first().content, "application/base64,ZmlsZV9jb250ZW50")
        
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
        self.assertTrue(Posts.objects.all().count(), 0)

    def test_multiple_files(self):
        author_id = str(self.author1.id)
        data = {
            "author": author_id,
            "title": "wild",
            "contentType": "text/plain"
        }
        post_data = json.dumps(data)
        fp = SimpleUploadedFile("file.jpg", b"file_content", content_type="image/jpeg")
        fp2 = SimpleUploadedFile("file2.jpg", b"file_content", content_type="image/png")
        response = self.client.post('/posts/', {'imageFiles': {fp, fp2}, 'query': 'createpost', 'postData': post_data})
        self.assertEqual(response.status_code, 200)

        self.assertEqual(len(Posts.objects.filter(author=author_id)), 3)
        
        text_post = Posts.objects.filter(contentType="text/plain")
        self.assertEqual(len(text_post), 1)

        # Checks the post_id attribute to make sure it matches the actual text post
        image_posts = Posts.objects.filter(post_id=text_post[0].post_id, contentType__icontains="image/")
        self.assertEqual(len(image_posts), 2)

        # Checks the content of each image (base64 encoded)
        self.assertEqual(Posts.objects.get(contentType="image/jpeg;base64").content, "image/jpeg;base64,ZmlsZV9jb250ZW50")
        self.assertEqual(Posts.objects.get(contentType="image/png;base64").content, "image/png;base64,ZmlsZV9jb250ZW50")

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
        self.assertEqual(res.status_code, 403)
        self.assertEqual(len(Posts.objects.all()), 1)
        
    def test_deletion_wrong_user_authentication(self):
        self.client.login(username="user2", password="password")
        post = Posts.objects.create(author=self.author1)
        res = self.client.delete("/posts/{0}/".format(post.id))
        self.assertEqual(res.status_code, 403)
        self.assertEqual(len(Posts.objects.all()), 1)

    def test_put_unauthenticated(self):
        self.client.logout()
        post = Posts.objects.create(author=self.author1, title="one")
        response = self.client.put("/posts/{0}/".format(post.id), json.dumps({
            "title": "new title",
            "unlisted": False,
            "contentType": "text/markdown",
            "description": "Hello",
            "author": str(self.author1.id)
        }), content_type='application/json')
        self.assertEqual(response.status_code, 403)
        self.assertEqual(Posts.objects.all().first().title, "one")
        
    def test_put_wrong_user(self):
        self.client.login(username="user2", password="password")
        post = Posts.objects.create(author=self.author1, title="one")
        response = self.client.put("/posts/{0}/".format(post.id), json.dumps({
            "title": "new title",
            "unlisted": False,
            "contentType": "text/markdown",
            "description": "Hello",
            "author": str(self.author1.id)
        }), content_type='application/json')
        self.assertEqual(response.status_code, 403)
        self.assertEqual(Posts.objects.all().first().title, "one")
        
    def test_put_valid(self):
        post = Posts.objects.create(author=self.author1, title="one")
        response = self.client.put("/posts/{0}/".format(post.id), json.dumps({
            "title": "new title",
            "unlisted": False,
            "contentType": "text/markdown",
            "description": "Hello",
            "content": "Test post content",
            "author": str(self.author1.id)
        }), content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        
        posts = Posts.objects.all()
        new_post = posts.first()
        
        self.assertEqual(posts.count(), 1)
        self.assertEqual(new_post.title, "new title")
        self.assertEqual(new_post.unlisted, False)
        self.assertEqual(new_post.contentType, "text/markdown")
        self.assertEqual(new_post.description, "Hello")
        self.assertEqual(new_post.content, "Test post content")
        self.assertEqual(new_post.author, self.author1)
