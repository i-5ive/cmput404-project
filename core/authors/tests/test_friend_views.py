from django.test import TestCase
from django.urls import reverse

from core.authors.models import Follow
from core.authors.views import AuthorViewSet

import unittest
from unittest.mock import patch

from core.authors.util import get_author_url
from core.authors.tests.util import setupUser

def get_friends_path(userId):
    view = AuthorViewSet()
    view.basename = "author"
    view.request = None
    return view.reverse_action("friends", args=[userId])

class ListFriendsViewTests(TestCase):

    def setUp(self):
        self.author1 = setupUser("yeet")
        self.author2 = setupUser("yaw")
        self.author3 = setupUser("yaw2")

    def test_invalid_user(self):
        deletedId = str(self.author1.id)
        self.author1.delete()
        response = self.client.get(get_friends_path(deletedId))
        self.assertEqual(response.status_code, 404)

    def test_no_friends(self):
        response = self.client.get(get_friends_path(str(self.author1.id)))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["query"], "friends")
        self.assertEqual(len(response.data["authors"]), 0)

    def test_one_follow(self):
        author1Url = get_author_url(str(self.author1.id))
        author2Url = get_author_url(str(self.author2.id))

        Follow.objects.create(follower=author2Url, followed=author1Url)

        response = self.client.get(get_friends_path(str(self.author1.id)))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["query"], "friends")
        self.assertEqual(len(response.data["authors"]), 0)

    def test_one_friend(self):
        author1Url = get_author_url(str(self.author1.id))
        author2Url = get_author_url(str(self.author2.id))

        Follow.objects.create(follower=author2Url, followed=author1Url)
        Follow.objects.create(follower=author1Url, followed=author2Url)

        response = self.client.get(get_friends_path(str(self.author1.id)))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["query"], "friends")
        self.assertEqual(len(response.data["authors"]), 1)
        self.assertEqual(response.data["authors"][0], author2Url)

        response = self.client.get(get_friends_path(str(self.author2.id)))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["query"], "friends")
        self.assertEqual(len(response.data["authors"]), 1)
        self.assertEqual(response.data["authors"][0], author1Url)

    def test_two_friends(self):
        author1Url = get_author_url(str(self.author1.id))
        author2Url = get_author_url(str(self.author2.id))
        author3Url = get_author_url(str(self.author3.id))

        Follow.objects.create(follower=author2Url, followed=author1Url)
        Follow.objects.create(follower=author1Url, followed=author2Url)
        Follow.objects.create(follower=author3Url, followed=author1Url)
        Follow.objects.create(follower=author1Url, followed=author3Url)

        response = self.client.get(get_friends_path(str(self.author1.id)))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["query"], "friends")
        self.assertEqual(len(response.data["authors"]), 2)
        self.assertTrue(author2Url in response.data["authors"])
        self.assertTrue(author3Url in response.data["authors"])

        response = self.client.get(get_friends_path(str(self.author2.id)))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["authors"]), 1)
        self.assertEqual(response.data["authors"][0], author1Url)

        response = self.client.get(get_friends_path(str(self.author3.id)))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["authors"]), 1)
        self.assertEqual(response.data["authors"][0], author1Url)

    def test_one_follow_one_friend(self):
        author1Url = get_author_url(str(self.author1.id))
        author2Url = get_author_url(str(self.author2.id))
        author3Url = get_author_url(str(self.author3.id))

        Follow.objects.create(follower=author2Url, followed=author1Url)
        Follow.objects.create(follower=author1Url, followed=author2Url)
        Follow.objects.create(follower=author1Url, followed=author3Url)

        response = self.client.get(get_friends_path(str(self.author1.id)))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["query"], "friends")
        self.assertEqual(len(response.data["authors"]), 1)
        self.assertEqual(response.data["authors"][0], author2Url)

        response = self.client.get(get_friends_path(str(self.author2.id)))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["authors"]), 1)
        self.assertEqual(response.data["authors"][0], author1Url)

def get_friends_with_any_body(userId, friends):
    return {
        "query": "friends",
        "author": get_author_url(str(userId)),
        "authors": friends
    }

class CheckFriendsViewTests(TestCase):

    def setUp(self):
        self.author1 = setupUser("yeet")
        self.author2 = setupUser("yaw")
        self.author3 = setupUser("yaw2")

    def test_invalid_user(self):
        deletedId = str(self.author1.id)
        self.author1.delete()
        data = get_friends_with_any_body(deletedId, [])
        response = self.client.post(get_friends_path(deletedId), data, content_type="application/json")
        self.assertEqual(response.status_code, 404)

    @patch("core.authors.friends_util.get_friends_set")
    def test_no_friends(self, friends_set_mock):
        friends_set_mock.return_value = set()

        data = get_friends_with_any_body(str(self.author1.id), [])
        response = self.client.post(get_friends_path(str(self.author1.id)), data, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["query"], "friends")
        self.assertEqual(len(response.data["authors"]), 0)
        self.assertEqual(response.data["author"], get_author_url(str(self.author1.id)))

    @patch("core.authors.friends_util.get_friends_set")
    def test_no_matching_friends_empty_set(self, friends_set_mock):
        friends_set_mock.return_value = set()

        data = get_friends_with_any_body(str(self.author1.id), ["http://127.0.0.1:8000/author/yeet"])
        response = self.client.post(get_friends_path(str(self.author1.id)), data, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["query"], "friends")
        self.assertEqual(len(response.data["authors"]), 0)
        self.assertEqual(response.data["author"], get_author_url(str(self.author1.id)))

    @patch("core.authors.friends_util.get_friends_set")
    def test_no_matching_friends(self, friends_set_mock):
        friends_set_mock.return_value = set(["http://127.0.0.1:8000/author/yaw"])

        data = get_friends_with_any_body(str(self.author1.id), ["http://127.0.0.1:8000/author/yeet"])
        response = self.client.post(get_friends_path(str(self.author1.id)), data, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["query"], "friends")
        self.assertEqual(len(response.data["authors"]), 0)
        self.assertEqual(response.data["author"], get_author_url(str(self.author1.id)))

    @patch("core.authors.friends_view.get_friends_set")
    def test_one_friend(self, friends_set_mock):

        commonAuthor = "http://127.0.0.1:8000/author/yeet"
        friends_set_mock.return_value = set([commonAuthor])

        data = get_friends_with_any_body(str(self.author1.id), [commonAuthor, "http://127.0.0.1:8000/author/yaw"])
        response = self.client.post(get_friends_path(str(self.author1.id)), data, content_type="application/json")
       
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["query"], "friends")
        self.assertEqual(len(response.data["authors"]), 1)
        self.assertEqual(response.data["authors"][0], commonAuthor)
        self.assertEqual(response.data["author"], get_author_url(str(self.author1.id)))

    @patch("core.authors.friends_view.get_friends_set")
    def test_two_friends(self, friends_set_mock):
        commonAuthor = "http://127.0.0.1:8000/author/yeet"
        commonAuthor2 = "http://127.0.0.1:8000/author/yyy"
        friends_set_mock.return_value = set([commonAuthor, commonAuthor2])

        data = get_friends_with_any_body(str(self.author1.id), [commonAuthor, commonAuthor2, "http://127.0.0.1:8000/author/yaw"])
        response = self.client.post(get_friends_path(str(self.author1.id)), data, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["query"], "friends")
        self.assertEqual(len(response.data["authors"]), 2)
        self.assertTrue(commonAuthor in response.data["authors"])
        self.assertTrue(commonAuthor2 in response.data["authors"])
        self.assertEqual(response.data["author"], get_author_url(str(self.author1.id)))