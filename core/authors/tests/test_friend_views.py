import json

from django.test import TestCase
from django.urls import reverse

from core.authors.models import Author, Follow
from core.users.models import User
from core.authors.views import AuthorViewSet

import unittest
from unittest.mock import patch

from core.authors.util import get_author_url

def setupUser(username):
    user = User.objects.create(username=username)
    return Author.objects.get(user=user)

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
        pass

    def test_post(self):
        pass

    def test_no_friends(self):
        response = self.client.get(get_friends_path(str(self.author1.id)))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["query"], "friends")
        self.assertEqual(len(response.data["authors"]), 0)

    def test_one_follow(self):
        pass

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

    def test_two_friends(self):
        pass

    def test_two_friends_diff_users(self):
        pass
