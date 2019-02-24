import json

from django.test import Client, TestCase
from django.core.files.uploadedfile import SimpleUploadedFile

from core.posts.models import Posts
from core.authors.util import get_author_id
from core.authors.tests.util import setupUser

class PostViewsTest(TestCase):

    def setUp(self):
        self.author1 = setupUser("cry")

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
        response = self.client.post('/posts/', {'postData': post_data})
        self.assertEqual(response.status_code, 200)
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
        response = self.client.post('/posts/', {'imageFiles': fp, 'postData': post_data})
        self.assertEqual(response.status_code, 200)

    def test_invalid_file_type(self):
        author_id = str(self.author1.id)
        data = {
            "author": author_id,
            "title": "wild"
        }
        post_data = json.dumps(data)
        fp = SimpleUploadedFile("file.mp4", b"file_content", content_type="video/mp4")
        response = self.client.post('/posts/', {'imageFiles': fp, 'postData': post_data})
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
        response = self.client.post('/posts/', {'imageFiles': {fp, fp2}, 'postData': post_data})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(Posts.objects.filter(author=author_id)), 3)
    
    def test_delete_post(self):
        author_id = str(self.author1.id)
        data = {
            "author": author_id,
            "title": "wild"
        }
        post_data = json.dumps(data)
        response = self.client.post('/posts/', {'postData': post_data})

        post = Posts.objects.get(author=author_id)
        response = self.client.delete(f'/posts/{post.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["message"], "Post deleted successfully")
        self.assertEqual(len(Posts.objects.filter(id=post.id)), 0)


