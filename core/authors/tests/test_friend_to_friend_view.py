from urllib.parse import quote
from django.test import TestCase

from core.authors.models import Follow

from core.authors.util import get_author_url
from core.authors.tests.util import setupUser

def get_friends_path(userId, otherId):
    return "/author/" + str(userId) + "/friends/" + str(otherId) + "/"

class TestFriendToFriendView(TestCase):

    def setUp(self):
        self.author1 = setupUser("yeet")
        self.author2 = setupUser("yaw")
        self.author3 = setupUser("yaw2")

    def test_first_user_invalid(self):
        deletedId = str(self.author1.id)
        self.author1.delete()
        response = self.client.get(get_friends_path(deletedId, self.author2.id))
        self.assertEqual(response.status_code, 404)

    def test_second_user_invalid(self):
        deletedId = str(self.author1.id)
        deletedUrl = self.author1.get_url()
        self.author1.delete()
        response = self.client.get(get_friends_path(self.author2.id, deletedId))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["query"], "friends")
        self.assertEqual(response.data["authors"], [self.author2.get_url(), deletedUrl])
        self.assertFalse(response.data["friends"])
        
    def test_not_friends(self):
        response = self.client.get(get_friends_path(self.author1.id, self.author2.id))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["query"], "friends")
        self.assertEqual(response.data["authors"], [self.author1.get_url(), self.author2.get_url()])
        self.assertFalse(response.data["friends"])

    def test_follow(self):
        Follow.objects.create(follower=self.author1.get_url(), followed=self.author2.get_url())
        response = self.client.get(get_friends_path(self.author1.id, self.author2.id))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["query"], "friends")
        self.assertEqual(response.data["authors"], [self.author1.get_url(), self.author2.get_url()])
        self.assertFalse(response.data["friends"])
        
    def test_reverse_follow(self):
        Follow.objects.create(follower=self.author2.get_url(), followed=self.author1.get_url())
        response = self.client.get(get_friends_path(self.author1.id, self.author2.id))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["query"], "friends")
        self.assertEqual(response.data["authors"], [self.author1.get_url(), self.author2.get_url()])
        self.assertFalse(response.data["friends"])
        
    def test_friends(self):
        Follow.objects.create(follower=self.author1.get_url(), followed=self.author2.get_url())
        Follow.objects.create(follower=self.author2.get_url(), followed=self.author1.get_url())
        response = self.client.get(get_friends_path(self.author1.id, self.author2.id))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["query"], "friends")
        self.assertEqual(response.data["authors"], [self.author1.get_url(), self.author2.get_url()])
        self.assertTrue(response.data["friends"])

    def test_friends_external_author(self):
        external_url = "https://google.ca/author/89222"
        Follow.objects.create(follower=external_url, followed=self.author2.get_url())
        Follow.objects.create(follower=self.author2.get_url(), followed=external_url)
        escaped_url = quote(external_url, safe='~()*!.\'')
        
        response = self.client.get(get_friends_path(self.author2.id, escaped_url))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["query"], "friends")
        self.assertEqual(response.data["authors"], [self.author2.get_url(), external_url])
        self.assertTrue(response.data["friends"])

    def test_friends_reverse_order(self):
        Follow.objects.create(follower=self.author1.get_url(), followed=self.author2.get_url())
        Follow.objects.create(follower=self.author2.get_url(), followed=self.author1.get_url())
        response = self.client.get(get_friends_path(self.author2.id, self.author1.id))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["query"], "friends")
        self.assertEqual(response.data["authors"], [self.author2.get_url(), self.author1.get_url()])
        self.assertTrue(response.data["friends"])
        
    def test_other_author_not_friends(self):
        Follow.objects.create(follower=self.author1.get_url(), followed=self.author2.get_url())
        Follow.objects.create(follower=self.author2.get_url(), followed=self.author1.get_url())
        Follow.objects.create(follower=self.author1.get_url(), followed=self.author3.get_url())
        
        response = self.client.get(get_friends_path(self.author1.id, self.author3.id))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["query"], "friends")
        self.assertEqual(response.data["authors"], [self.author1.get_url(), self.author3.get_url()])
        self.assertFalse(response.data["friends"])
