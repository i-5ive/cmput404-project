from django.test import Client, TestCase
from django.urls import reverse

import unittest
import json
from unittest.mock import patch
from django.core.files.uploadedfile import SimpleUploadedFile


from core.authors.util import get_author_id
from core.authors.tests.util import setupUser

class PostViewsTest(TestCase):

    def setUp(self):
        self.author1 = setupUser("cry")

    def test_invalid_query(self):
        response = self.client.post('/handleposts/', {'query': 'ihateposts'})
        self.assertEqual(response.status_code, 400)

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
        response = self.client.post('/handleposts/', {'query': 'createpost', 'post_data': post_data})
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
        response = self.client.post('/handleposts/', {'imageFiles': fp, 'query': 'createpost', 'post_data': post_data})
        self.assertEqual(response.status_code, 200)

    def test_invalid_file_type(self):
        author_id = str(self.author1.id)
        data = {
            "author": author_id,
            "title": "wild"
        }
        post_data = json.dumps(data)
        fp = SimpleUploadedFile("file.mp4", b"file_content", content_type="video/mp4")
        response = self.client.post('/handleposts/', {'imageFiles': fp, 'query': 'createpost', 'post_data': post_data})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["message"], "Invalid file type")

    def test_multiple_files(self):
        pass
    
    def test_delete_post(self):
        pass