from django.test import TestCase

from core.authors.tests.util import setupUser
from core.posts.models import Posts, Comments
from core.hostUtil import get_host_url

def date_to_str(date):
    return str(date).replace("+00:00", "Z").replace(" ", "T")

class CommentsViewTests(TestCase):

    def setUp(self):
        self.author1 = setupUser("cry", "password")
        self.client.login(username="cry", password="password")

    def test_unauthenticated_non_public(self):
        self.client.logout()
        post = Posts.objects.create(visibility="PRIVATE", author=self.author1)
        res = self.client.get("/posts/{0}/comments/".format(post.id))
        self.assertEqual(res.status_code, 401)
        
    def test_unauthenticated_public_post(self):
        post = Posts.objects.create(visibility="PUBLIC", author=self.author1)
        res = self.client.get("/posts/{0}/comments/".format(post.id))
        self.assertEqual(res.data, {
            "query": "comments",
            "count": 0,
            "size": 5,
            "comments": []
        })
    
    def test_last_page(self):
        post = Posts.objects.create(visibility="PUBLIC", author=self.author1)
        comments = []
        for i in range(0, 100):
            comments.append(Comments.objects.create(post=post, comment="Hello{0}".format(i), author=self.author1))
        res = self.client.get("/posts/{0}/comments/".format(post.id), {"page": 19})
        self.assertEqual(res.status_code, 200)

        author_details = {
            "id": self.author1.get_url(),
            "url": self.author1.get_url(),
            "host": get_host_url(),
            "displayName": self.author1.get_display_name()
        }
        expected_comments = []
        for i in range(4, -1, -1):
            expected_comments.append(
                {
                    "author": author_details,
                    "comment": comments[i].comment,
                    "contentType": comments[i].contentType,
                    "published": date_to_str(comments[i].published),
                    "id": str(comments[i].id)
                }
            )
        self.assertEqual(res.json(), {
            "query": "comments",
            "count": 100,
            "size": 5,
            "previous": "http://testserver/posts/{0}/comments/?page=18".format(post.id),
            "comments": expected_comments
        })
        
    def test_first_page(self):
        post = Posts.objects.create(visibility="PUBLIC", author=self.author1)
        comments = []
        for i in range(0, 100):
            comments.append(Comments.objects.create(post=post, comment="Hello{0}".format(i), author=self.author1))
        res = self.client.get("/posts/{0}/comments/".format(post.id), {"page": 0})
        self.assertEqual(res.status_code, 200)
        
        author_details = {
            "id": self.author1.get_url(),
            "url": self.author1.get_url(),
            "host": get_host_url(),
            "displayName": self.author1.get_display_name()
        }
        expected_comments = []
        for i in range(99, 94, -1):
            expected_comments.append(
                {
                    "author": author_details,
                    "comment": comments[i].comment,
                    "contentType": comments[i].contentType,
                    "published": date_to_str(comments[i].published),
                    "id": str(comments[i].id)
                }
            )
        self.assertEqual(res.json(), {
            "query": "comments",
            "count": 100,
            "size": 5,
            "next": "http://testserver/posts/{0}/comments/?page=1".format(post.id),
            "comments": expected_comments
        })
        
    def test_next_and_prev_page(self):
        post = Posts.objects.create(visibility="PUBLIC", author=self.author1)
        comments = []
        for i in range(0, 100):
            comments.append(Comments.objects.create(post=post, comment="Hello{0}".format(i), author=self.author1))
        res = self.client.get("/posts/{0}/comments/".format(post.id), {"page": 10})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data["previous"], "http://testserver/posts/{0}/comments/?page=9".format(post.id))
        self.assertEqual(res.data["next"], "http://testserver/posts/{0}/comments/?page=11".format(post.id))

    def test_empty_page(self):
        post = Posts.objects.create(visibility="PUBLIC", author=self.author1)
        res = self.client.get("/posts/{0}/comments/".format(post.id), {"page": 0})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.data["comments"]), 0)
        
    def test_invalid_page(self):
        post = Posts.objects.create(visibility="PRIVATE", author=self.author1)
        comments = []
        for i in range(0, 100):
            comments.append(Comments.objects.create(post=post, comment="Hello{0}".format(i), author=self.author1))
        res = self.client.get("/posts/{0}/comments/".format(post.id), {"page": -1})
        self.assertEqual(res.status_code, 400)
        
    def test_invalid_size(self):
        post = Posts.objects.create(visibility="PRIVATE", author=self.author1)
        comments = []
        for i in range(0, 100):
            comments.append(Comments.objects.create(post=post, comment="Hello{0}".format(i), author=self.author1))
        res = self.client.get("/posts/{0}/comments/".format(post.id), {"page": 1, "size": -1})
        self.assertEqual(res.status_code, 400)

    def test_custom_size(self):
        post = Posts.objects.create(visibility="PUBLIC", author=self.author1)
        comments = []
        for i in range(0, 100):
            comments.append(Comments.objects.create(post=post, comment="Hello{0}".format(i), author=self.author1))
        res = self.client.get("/posts/{0}/comments/".format(post.id), {"page": 0, "size": 25})
        self.assertEqual(res.status_code, 200)

        author_details = {
            "id": self.author1.get_url(),
            "url": self.author1.get_url(),
            "host": get_host_url(),
            "displayName": self.author1.get_display_name()
        }
        expected_comments = []
        for i in range(99, 74, -1):
            expected_comments.append(
                {
                    "author": author_details,
                    "comment": comments[i].comment,
                    "contentType": comments[i].contentType,
                    "published": date_to_str(comments[i].published),
                    "id": str(comments[i].id)
                }
            )
        self.assertEqual(res.json(), {
            "query": "comments",
            "count": 100,
            "size": 25,
            "next": "http://testserver/posts/{0}/comments/?page=1".format(post.id),
            "comments": expected_comments
        })