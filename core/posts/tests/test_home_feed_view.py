from django.test import TestCase

from core.authors.tests.util import setupUser
from core.posts.models import Posts
from core.authors.models import Follow

class HomeFeedViewTests(TestCase):

    def setUp(self):
        self.author1 = setupUser("cry", "password")
        self.author2 = setupUser("user2", "password")
        self.client.login(username="cry", password="password")

    def test_unauthenticated(self):
        self.client.logout()
        for i in range(0, 50):
            Posts.objects.create(author=self.author1, visibility="PUBLIC", title=str(i))
        
        res = self.client.get("/posts/feed/")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data["count"], 50)
        self.assertEqual(res.data["next"], "http://testserver/posts/feed/?page=1")
        self.assertEqual(len(res.data["posts"]), res.data["size"])
        self.assertGreater(res.data["size"], 0)
        self.assertIsNone(res.data.get("previous"))
        
        i = 49
        for post in res.data["posts"]:
            self.assertEqual(post["title"], str(i))
            i -= 1
        
    def test_no_results(self):
        res = self.client.get("/posts/feed/")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data["count"], 0)
        self.assertIsNone(res.data.get("next"))
        self.assertIsNone(res.data.get("previous"))
        self.assertEqual(len(res.data["posts"]), 0)
        
    def test_invalid_page(self):
        res = self.client.get("/posts/feed/", {"page": -1})
        self.assertEqual(res.status_code, 400)
        
    def test_invalid_size(self):
        res = self.client.get("/posts/feed/", {"size": -1})
        self.assertEqual(res.status_code, 400)
        
    def test_last_page(self):
        self.client.logout()
        for i in range(0, 50):
            Posts.objects.create(author=self.author1, visibility="PUBLIC", title=str(i))
        
        res = self.client.get("/posts/feed/", {"page": 1})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data["count"], 50)
        self.assertEqual(res.data["previous"], "http://testserver/posts/feed/?page=0")
        self.assertEqual(len(res.data["posts"]), res.data["size"])
        self.assertGreater(res.data["size"], 0)
        self.assertIsNone(res.data.get("next"))
        
        i = 24
        for post in res.data["posts"]:
            self.assertEqual(post["title"], str(i))
            i -= 1
        
    def test_include_follows(self):
        for i in range(0, 50):
            Posts.objects.create(author=self.author2, visibility="PUBLIC")
        Follow.objects.create(follower=self.author1.get_url(), followed=self.author2.get_url())
        
        res = self.client.get("/posts/feed/")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data["count"], 50)
    
    def test_follows_no_private(self):
        for i in range(0, 50):
            Posts.objects.create(author=self.author2, visibility="PRIVATE")
        Follow.objects.create(follower=self.author1.get_url(), followed=self.author2.get_url())
        
        res = self.client.get("/posts/feed/")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data["count"], 0)
        
    def test_follows_private_visible_to(self):
        for i in range(0, 50):
            Posts.objects.create(author=self.author2, visibility="PRIVATE", visibleTo=[self.author1.get_url()])
        Follow.objects.create(follower=self.author1.get_url(), followed=self.author2.get_url())
        
        res = self.client.get("/posts/feed/")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data["count"], 50)
        
    def test_include_own(self):
        for i in range(0, 50):
            Posts.objects.create(author=self.author1, visibility="PRIVATE")
        
        res = self.client.get("/posts/feed/")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data["count"], 50)

    def test_own_and_followed(self):
        for i in range(0, 50):
            Posts.objects.create(author=self.author1, visibility="PRIVATE")
        for i in range(0, 50):
            Posts.objects.create(author=self.author2, visibility="PRIVATE", visibleTo=[self.author1.get_url()])
        Follow.objects.create(follower=self.author1.get_url(), followed=self.author2.get_url())
        
        res = self.client.get("/posts/feed/")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data["count"], 100)
