from django.test import TestCase

from core.authors.models import Author, Follow
from core.users.models import User
from core.authors.views import AuthorViewSet

from core.authors.util import get_author_url
from core.authors.tests.util import setupUser

def get_body(id):
    return {
        "author": id
    }

def get_path(userId):
    if ("/author/" in userId):
        userId = userId.split("/author/")[1]

    view = AuthorViewSet()
    view.basename = "author"
    view.request = None
    return view.reverse_action("is_following", args=[userId])

class FollowCheckTest(TestCase):

    def setUp(self):
        self.author1 = get_author_url(str(setupUser("one").id))
        self.author2 = get_author_url(str(setupUser("two").id))
        self.author3 = get_author_url(str(setupUser("three").id))

    def test_invalid_user(self):
        author = setupUser("test")
        deletedId = str(author.id)
        author.delete()

        response = self.client.post(get_path(deletedId), data=get_body(get_author_url(deletedId)), content_type="application/json")
        self.assertEqual(response.status_code, 404)

    def test_following_success(self):
        Follow.objects.create(followed=self.author2, follower=self.author1)

        body = get_body(self.author2)
        response = self.client.post(get_path(self.author1), data=body, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data["isFollowingUser"])

    def test_following_success_no_url(self):
        Follow.objects.create(followed=self.author2, follower=self.author1)

        body = get_body(self.author2.split("/author/")[1])
        response = self.client.post(get_path(self.author1), data=body, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data["isFollowingUser"])

    def test_not_following(self):
        body = get_body(self.author2)
        response = self.client.post(get_path(self.author1), data=body, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.data["isFollowingUser"])

    def test_inverse_following(self):
        Follow.objects.create(follower=self.author2, followed=self.author1)

        body = get_body(self.author2)
        response = self.client.post(get_path(self.author1), data=body, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.data["isFollowingUser"])