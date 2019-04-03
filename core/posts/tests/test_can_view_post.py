from django.test import TestCase

from core.posts.models import Posts
from core.authors.models import Author, Follow

from core.authors.tests.util import setupUser
from core.posts.util import can_user_view

class MockUnauthenticatedUser:
    def __init__(self, url):
        self.is_authenticated = False
        self.url = url
        
    def get_url(self):
        return self.url

def make_friends(one, two):
    Follow.objects.create(follower=one.get_url(), followed=two.get_url())
    Follow.objects.create(followed=one.get_url(), follower=two.get_url())
        
class CanViewPostTests(TestCase):

    def setUp(self):
        self.author1 = setupUser("cry", "password")
        self.author2 = setupUser("user2", "password")
        self.author3 = setupUser("user3", "password")
        
    def test_visible(self):
        post = Posts.objects.create(**{
            'title': 'Hello World',
            'author': self.author1,
            'visibility': "PUBLIC"
        })
        
        self.assertTrue(can_user_view(self.author2.user, post))
        
    def test_server_only(self):
        post = Posts.objects.create(**{
            'title': 'Hello World',
            'author': self.author1,
            'visibility': "SERVERONLY"
        })
        
        self.assertFalse(can_user_view(self.author2.user, post))
        
    def test_private_not_allowed(self):
        post = Posts.objects.create(**{
            'title': 'Hello World',
            'author': self.author1,
            'visibility': "PRIVATE"
        })
        
        self.assertFalse(can_user_view(self.author2.user, post))
        
    def test_private_allowed(self):
        post = Posts.objects.create(**{
            'title': 'Hello World',
            'author': self.author1,
            'visibility': "PRIVATE",
            "visibleTo": [self.author2.get_url()]
        })
        
        self.assertTrue(can_user_view(self.author2.user, post))
        
    def test_friend_allowed(self):
        post = Posts.objects.create(**{
            'title': 'Hello World',
            'author': self.author1,
            'visibility': "FRIENDS"
        })
        
        make_friends(self.author1, self.author2)
        self.assertTrue(can_user_view(self.author2.user, post))
        
    def test_server_only_allowed(self):
        post = Posts.objects.create(**{
            'title': 'Hello World',
            'author': self.author1,
            'visibility': "SERVERONLY"
        })
        
        make_friends(self.author1, self.author2)
        self.assertTrue(can_user_view(self.author2.user, post))

    def test_friend_not_allowed(self):
        post = Posts.objects.create(**{
            'title': 'Hello World',
            'author': self.author1,
            'visibility': "FRIENDS"
        })
        
        self.assertFalse(can_user_view(self.author2.user, post))
        
    def test_author(self):
        post = Posts.objects.create(**{
            'title': 'Hello World',
            'author': self.author1,
            'visibility': "PRIVATE"
        })
        
        self.assertTrue(can_user_view(self.author1.user, post))
        
    def test_non_public_unauthenticated(self):
        post = Posts.objects.create(**{
            'title': 'Hello World',
            'author': self.author1,
            'visibility': "PRIVATE",
            "visibleTo": [self.author2.get_url()]
        })
        
        self.assertFalse(can_user_view(MockUnauthenticatedUser(self.author2.get_url()), post))
        
    def test_foaf_mutual(self):
        post = Posts.objects.create(**{
            'title': 'Hello World',
            'author': self.author3,
            'visibility': "FOAF"
        })
        
        make_friends(self.author1, self.author2)
        make_friends(self.author2, self.author3)
        self.assertTrue(can_user_view(self.author1.user, post))
        
    def test_foaf_no_mutual(self):
        post = Posts.objects.create(**{
            'title': 'Hello World',
            'author': self.author3,
            'visibility': "FOAF"
        })
        
        make_friends(self.author2, self.author3)
        self.assertFalse(can_user_view(self.author1.user, post))
        
    def test_foaf_author_mutual(self):
        post = Posts.objects.create(**{
            'title': 'Hello World',
            'author': self.author3,
            'visibility': "FOAF"
        })
        
        make_friends(self.author2, self.author3)
        make_friends(self.author3, self.author1)
        make_friends(self.author1, self.author2)
        
        self.assertTrue(can_user_view(self.author2.user, post))
