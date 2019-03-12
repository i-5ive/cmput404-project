from django.test import TestCase

from core.authors.tests.util import setupUser, createPostForAuthor

class TestAuthorPost(TestCase):
    def setUp(self):
        self.author1 = setUpUser("user1_tap")
        self.author2 = setUpUser("user2_tap")
        self.author3 = setUpUser("user3_tap")