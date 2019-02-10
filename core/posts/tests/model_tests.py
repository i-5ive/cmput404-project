from django.test import TestCase

from core.posts.models import Posts


class AuthorModelTest(TestCase):

    def setUp(self):
        pass

    def test_create_post(self):
        post = Posts.objects.create(**{
            'title': 'Hello World',
        })
        self.assertIsNotNone(post)
