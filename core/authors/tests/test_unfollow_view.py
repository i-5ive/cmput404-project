from django.test import TestCase
from django.urls import reverse

from core.authors.models import Author, Follow, FriendRequest

import unittest
from unittest.mock import patch

from core.authors.util import get_author_url
from core.authors.tests.util import setupUser
from core.authors.unfollow_author_view import QUERY

def get_body(author1, author2, query=QUERY):
    return {
        "query": query,
        "author": {
            "id": author1,
            "host": "http://127.0.0.1",
            "displayName": "Some random name",
            "url": author1
        },
        "requester": {
            "id": author2,
            "host": "http://127.0.0.1",
            "displayName": "Some random name 2",
            "url": author2
        }
    }

class UnfollowViewTest(TestCase):

    def setUp(self):
        self.author1 = get_author_url(str(setupUser("yeet", "password").id))
        self.author2 = get_author_url(str(setupUser("yaw", "password").id))
        self.author3 = get_author_url(str(setupUser("yaw2", "password").id))
        
        self.client.login(username="yeet", password="password")

    def test_wrong_user_authentication(self):
        Follow.objects.create(follower=self.author1, followed=self.author3)
        body = get_body(self.author3, self.author1)
        
        self.client.login(username="yaw2", password="password")
        response = self.client.post(reverse('unfollow'), data=body, content_type="application/json")

        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data["query"], QUERY)
        self.assertEqual(response.data["success"], False)
        
    def test_no_authentication(self):
        Follow.objects.create(follower=self.author1, followed=self.author3)
        body = get_body(self.author3, self.author1)
        
        self.client.logout()
        response = self.client.post(reverse('unfollow'), data=body, content_type="application/json")

        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data["query"], QUERY)
        self.assertEqual(response.data["success"], False)
        
    def test_get(self):
        response = self.client.get(reverse('unfollow'))
        self.assertEqual(response.status_code, 405)
        self.assertEqual(len(FriendRequest.objects.all()), 0)
        self.assertEqual(len(Follow.objects.all()), 0)

    def test_invalid_query(self):
        Follow.objects.create(follower=self.author1, followed=self.author3)
        body = get_body(self.author3, self.author1, query="NotFollow")
        response = self.client.post(reverse('unfollow'), data=body, content_type="application/json")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["query"], QUERY)
        self.assertEqual(response.data["success"], False)
        self.assertIsNotNone(response.data["message"])
        self.assertEqual(len(FriendRequest.objects.all()), 0)
        self.assertEqual(len(Follow.objects.all()), 1)

    def test_invalid_authors(self):
        Follow.objects.create(follower=self.author1, followed=self.author3)
        response = self.client.post(reverse('unfollow'), data={
            "query": QUERY,
            "author": "yyy",
            "requester": False
        }, content_type="application/json")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["query"], QUERY)
        self.assertEqual(response.data["success"], False)
        self.assertIsNotNone(response.data["message"])
        self.assertEqual(len(FriendRequest.objects.all()), 0)
        self.assertEqual(len(Follow.objects.all()), 1)

    def test_no_existing_follow(self):
        body = get_body(self.author3, self.author1)
        response = self.client.post(reverse('unfollow'), data=body, content_type="application/json")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["query"], QUERY)
        self.assertEqual(response.data["success"], False)
        self.assertIsNotNone(response.data["message"])
        self.assertEqual(len(FriendRequest.objects.all()), 0)
        self.assertEqual(len(Follow.objects.all()), 0)

    def test_inverse_follow(self):
        Follow.objects.create(follower=self.author3, followed=self.author1)
        body = get_body(self.author3, self.author1)
        response = self.client.post(reverse('unfollow'), data=body, content_type="application/json")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["query"], QUERY)
        self.assertEqual(response.data["success"], False)
        self.assertIsNotNone(response.data["message"])
        self.assertEqual(len(FriendRequest.objects.all()), 0)
        self.assertEqual(len(Follow.objects.all()), 1)

    def test_success_no_request(self):
        Follow.objects.create(follower=self.author1, followed=self.author3)
        body = get_body(self.author3, self.author1)
        response = self.client.post(reverse('unfollow'), data=body, content_type="application/json")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["query"], QUERY)
        self.assertEqual(response.data["success"], True)
        self.assertIsNotNone(response.data["message"])
        self.assertEqual(len(FriendRequest.objects.all()), 0)
        self.assertEqual(len(Follow.objects.all()), 0)

    def test_success_with_request(self):
        Follow.objects.create(follower=self.author1, followed=self.author3)
        FriendRequest.objects.create(requester=self.author1, friend=self.author3)
        body = get_body(self.author3, self.author1)
        response = self.client.post(reverse('unfollow'), data=body, content_type="application/json")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["query"], QUERY)
        self.assertEqual(response.data["success"], True)
        self.assertIsNotNone(response.data["message"])
        self.assertEqual(len(FriendRequest.objects.all()), 0)
        self.assertEqual(len(Follow.objects.all()), 0)

    def test_multiple_requests_success(self):
        Follow.objects.create(follower=self.author2, followed=self.author3)
        Follow.objects.create(follower=self.author1, followed=self.author3)
        FriendRequest.objects.create(requester=self.author1, friend=self.author3)
        FriendRequest.objects.create(requester=self.author2, friend=self.author3)

        body = get_body(self.author3, self.author1)
        response = self.client.post(reverse('unfollow'), data=body, content_type="application/json")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["query"], QUERY)
        self.assertEqual(response.data["success"], True)
        self.assertIsNotNone(response.data["message"])

        self.assertEqual(len(FriendRequest.objects.all()), 1)
        self.assertEqual(len(Follow.objects.all()), 1)
        self.assertIsNotNone(FriendRequest.objects.get(requester=self.author2, friend=self.author3))
        self.assertIsNotNone(Follow.objects.get(follower=self.author2, followed=self.author3))
