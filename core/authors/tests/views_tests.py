from django.test import TestCase
from django.urls import reverse

MINIMAL_AUTHOR_DATA = {
    "username": "testauthor",
    "password": "someSuperSecretPassword123"
}


class AuthorViewTests(TestCase):

    def setUp(self):
        pass

    def test_create_author_miminal_info(self):
        response = self.client.post(reverse('login'), data=MINIMAL_AUTHOR_DATA)
        print(response)
