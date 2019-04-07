import json

from django.test import TestCase
from django.urls import reverse

from core.authors.models import Author, Follow, FriendRequest
from core.users.models import User
from core.authors.views import AuthorViewSet

import unittest
from unittest.mock import patch

from core.authors.util import get_author_url
from core.authors.tests.util import setupUser

def get_local_authors_body(author1, author2, query="friendrequest"):
    return {
        "query": query,
        "author": {
            "id": "http://127.0.0.1:8000/author/" + str(author1.id),
            "host": "http://127.0.0.1:8000",
            "displayName": "Some random name",
            "url": "http://127.0.0.1:8000/author/" + str(author1.id)
        },
        "friend": {
            "id": "http://127.0.0.1:8000/author/" + str(author2.id),
            "host": "http://127.0.0.1:8000",
            "displayName": "Some random name 2",
            "url": "http://127.0.0.1:8000/author/" + str(author2.id)
        }
    }

class FriendRequestViewTestCase(TestCase):

    def setUp(self):
        self.author1 = setupUser("yeet", "password")
        self.author2 = setupUser("yaw", "password")
        self.author3 = setupUser("yaw2", "password")
        
        self.client.login(username="yeet", password="password")

    @patch("core.hostUtil.is_external_host")
    @patch("core.authors.util.get_author_id")
    def test_wrong_user_authenticated(self, author_id_mock, host_mock):
        self.client.login(username="yaw2", password="password")
        author_id_mock.side_effect = lambda x : x.split("/author/")[1]
        host_mock.return_value = False

        body = get_local_authors_body(self.author1, self.author2)
        response = self.client.post(reverse('friendrequest'), data=body, content_type="application/json")
        # Should check more than a response code..
        self.assertEqual(response.data["message"], "You must be authenticated as the requester to perform this action.")
        self.assertEqual(response.status_code, 403) 
        
    @patch("core.hostUtil.is_external_host")
    @patch("core.authors.util.get_author_id")
    def test_not_authenticated(self, author_id_mock, host_mock):
        self.client.logout()
        author_id_mock.side_effect = lambda x : x.split("/author/")[1]
        host_mock.return_value = False

        body = get_local_authors_body(self.author1, self.author2)
        response = self.client.post(reverse('friendrequest'), data=body, content_type="application/json")
        self.assertEqual(response.status_code, 403)
        
    def test_get(self):
        response = self.client.get(reverse('friendrequest'))
        self.assertEqual(response.status_code, 405)
        self.assertEqual(len(FriendRequest.objects.all()), 0)
        self.assertEqual(len(Follow.objects.all()), 0)

    def test_invalid_query(self):
        body = get_local_authors_body(self.author3, self.author1, query="NotFriendRequest")
        response = self.client.post(reverse('friendrequest'), data=body, content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["query"], "friendrequest")
        self.assertEqual(response.data["success"], False)
        self.assertIsNotNone(response.data["message"])
        self.assertEqual(len(FriendRequest.objects.all()), 0)
        self.assertEqual(len(Follow.objects.all()), 0)

    @patch("core.hostUtil.is_external_host")
    @patch("core.authors.util.get_author_id")
    def test_missing_author(self, author_id_mock, host_mock):
        author_id_mock.side_effect = lambda x : x.split("/author/")[1]
        host_mock.return_value = False

        body = get_local_authors_body(self.author3, self.author1)
        del body["author"]

        response = self.client.post(reverse('friendrequest'), data=body, content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["query"], "friendrequest")
        self.assertEqual(response.data["success"], False)
        self.assertIsNotNone(response.data["message"])
        self.assertEqual(len(FriendRequest.objects.all()), 0)
        self.assertEqual(len(Follow.objects.all()), 0)

    @patch("core.hostUtil.is_external_host")
    @patch("core.authors.util.get_author_id")
    def test_missing_friend(self, author_id_mock, host_mock):
        author_id_mock.side_effect = lambda x : x.split("/author/")[1]
        host_mock.return_value = False

        body = get_local_authors_body(self.author3, self.author1)
        del body["friend"]

        response = self.client.post(reverse('friendrequest'), data=body, content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["query"], "friendrequest")
        self.assertEqual(response.data["success"], False)
        self.assertIsNotNone(response.data["message"])
        self.assertEqual(len(FriendRequest.objects.all()), 0)
        self.assertEqual(len(Follow.objects.all()), 0)

    @patch("core.hostUtil.is_external_host")
    @patch("core.authors.util.get_author_id")
    def test_invalid_local_sender(self, author_id_mock, host_mock):
        author_id_mock.side_effect = lambda x : x.split("/author/")[1]
        host_mock.return_value = False

        body = get_local_authors_body(self.author3, self.author1)
        self.author3.delete()

        response = self.client.post(reverse('friendrequest'), data=body, content_type="application/json")
        # Should check more than a response code..
        self.assertEqual(response.data["message"], "You must be authenticated as the requester to perform this action.")
        self.assertEqual(response.status_code, 403) # Forbidden, technically you're trying to make friends for 2 other users
        self.assertEqual(len(FriendRequest.objects.all()), 0)
        self.assertEqual(len(Follow.objects.all()), 0)

    @patch("core.hostUtil.is_external_host")
    @patch("core.authors.util.get_author_id")
    def test_invalid_local_recepient(self, author_id_mock, host_mock):
        author_id_mock.side_effect = lambda x : x.split("/author/")[1]
        host_mock.return_value = False

        body = get_local_authors_body(self.author1, self.author3)
        self.author3.delete()

        response = self.client.post(reverse('friendrequest'), data=body, content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["query"], "friendrequest")
        self.assertEqual(response.data["success"], False)
        self.assertIsNotNone(response.data["message"])
        self.assertEqual(len(FriendRequest.objects.all()), 0)
        self.assertEqual(len(Follow.objects.all()), 0)

    @patch("core.hostUtil.is_external_host")
    @patch("core.authors.util.get_author_id")
    def test_same_user_request(self, author_id_mock, host_mock):
        author_id_mock.side_effect = lambda x : x.split("/author/")[1]
        host_mock.return_value = False

        response = self.client.post(reverse('friendrequest'), data=get_local_authors_body(self.author1, self.author1), content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["query"], "friendrequest")
        self.assertEqual(response.data["success"], False)
        self.assertIsNotNone(response.data["message"])
        self.assertEqual(len(FriendRequest.objects.all()), 0)
        self.assertEqual(len(Follow.objects.all()), 0)

    @patch("core.hostUtil.is_external_host")
    @patch("core.authors.util.get_author_id")
    def test_success_local_authors(self, author_id_mock, host_mock):
        author_id_mock.side_effect = lambda x : x.split("/author/")[1]
        host_mock.return_value = False

        body = get_local_authors_body(self.author1, self.author2)
        response = self.client.post(reverse('friendrequest'), data=body, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["query"], "friendrequest")
        self.assertEqual(response.data["success"], True)
        self.assertIsNotNone(response.data["message"])
        self.assertEqual(len(FriendRequest.objects.all()), 1)
        self.assertEqual(len(Follow.objects.all()), 1)

        self.assertIsNotNone(FriendRequest.objects.get(requester=body["author"]["url"], friend=body["friend"]["url"]))
        self.assertIsNotNone(Follow.objects.get(follower=body["author"]["url"], followed=body["friend"]["url"]))

    @patch("core.hostUtil.is_external_host")
    @patch("core.authors.util.get_author_id")
    def test_existing_request_local_authors(self, author_id_mock, host_mock):
        author_id_mock.side_effect = lambda x : x.split("/author/")[1]
        host_mock.return_value = False

        body = get_local_authors_body(self.author1, self.author2)

        res = self.client.post(reverse('friendrequest'), data=body, content_type="application/json")
        self.assertEqual(len(FriendRequest.objects.all()), 1)
        self.assertEqual(len(Follow.objects.all()), 1)

        response = self.client.post(reverse('friendrequest'), data=body, content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["query"], "friendrequest")
        self.assertEqual(response.data["success"], False)
        self.assertIsNotNone(response.data["message"])

        self.assertEqual(len(FriendRequest.objects.all()), 1)
        self.assertEqual(len(Follow.objects.all()), 1)

    @patch("core.hostUtil.is_external_host")
    @patch("core.authors.util.get_author_id")
    def test_success_local_authors_existing_follow(self, author_id_mock, host_mock):
        author_id_mock.side_effect = lambda x : x.split("/author/")[1]
        host_mock.return_value = False

        self.client.login(username="yaw", password="password")
        self.client.post(reverse('friendrequest'), data=get_local_authors_body(self.author2, self.author1), content_type="application/json")
        self.assertEqual(len(FriendRequest.objects.all()), 1)
        FriendRequest.objects.all()[0].delete()
        self.assertEqual(len(FriendRequest.objects.all()), 0)

        self.client.login(username="yeet", password="password")
        response = self.client.post(reverse('friendrequest'), data=get_local_authors_body(self.author1, self.author2), content_type="application/json")
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["query"], "friendrequest")
        self.assertEqual(response.data["success"], True)
        self.assertIsNotNone(response.data["message"])

        self.assertEqual(len(FriendRequest.objects.all()), 0)
        self.assertEqual(len(Follow.objects.all()), 2)

def get_pending_requests_path(userId):
    view = AuthorViewSet()
    view.basename = "author"
    view.request = None
    return view.reverse_action("friend_requests", args=[userId])

class PendingFriendRequestViewsTest(TestCase):

    def setUp(self):
        self.author1 = setupUser("one")
        self.author2 = setupUser("two")
        self.author3 = setupUser("three")
        self.author4 = setupUser("four")
        self.author5 = setupUser("five")

    def test_invalid_user(self):
        deletedId = self.author1.id
        self.author1.delete()
        response = self.client.get(get_pending_requests_path(str(deletedId)))
        self.assertEqual(response.status_code, 404)

    def test_post(self):
        response = self.client.post(get_pending_requests_path(str(self.author1.id)), data=json.dumps({}), content_type="application/json")
        self.assertEqual(response.status_code, 405)

    def test_no_friend_requests(self):
        response = self.client.get(get_pending_requests_path(str(self.author1.id)))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

    def test_one_friend_request(self):
        author1Url = get_author_url(str(self.author1.id))
        author2Url = get_author_url(str(self.author2.id))

        FriendRequest.objects.create(requester=author1Url, friend=author2Url)
        response = self.client.get(get_pending_requests_path(str(self.author2.id)))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0], {
            'displayName': self.author1.get_display_name(),
            'id': author1Url,
            'host': author1Url.split("/author/")[0],
            'url': author1Url
        })
    
    def test_one_friend_request_other_user(self):
        author1Url = get_author_url(str(self.author1.id))
        author2Url = get_author_url(str(self.author2.id))

        FriendRequest.objects.create(requester=author1Url, friend=author2Url)
        response = self.client.get(get_pending_requests_path(str(self.author1.id)))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

    def test_two_friend_requests(self):
        author1Url = get_author_url(str(self.author1.id))
        author2Url = get_author_url(str(self.author2.id))
        author3Url = get_author_url(str(self.author3.id))

        FriendRequest.objects.create(requester=author1Url, friend=author2Url)
        FriendRequest.objects.create(requester=author3Url, friend=author2Url)

        response = self.client.get(get_pending_requests_path(str(self.author2.id)))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        response.data.sort(key=lambda x : x["displayName"])
        self.assertEqual(response.data[0], {
            'displayName': self.author1.get_display_name(),
            'id': author1Url,
            'host': author1Url.split("/author/")[0],
            'url': author1Url
        })
        self.assertEqual(response.data[1], {
            'displayName': self.author3.get_display_name(),
            'id': author3Url,
            'host': author3Url.split("/author/")[0],
            'url': author3Url
        })

    def test_two_friend_requests_diff_users(self):
        author1Url = get_author_url(str(self.author1.id))
        author2Url = get_author_url(str(self.author2.id))
        author3Url = get_author_url(str(self.author3.id))

        FriendRequest.objects.create(requester=author1Url, friend=author2Url)
        FriendRequest.objects.create(requester=author3Url, friend=author1Url)

        response = self.client.get(get_pending_requests_path(str(self.author2.id)))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0], {
            'displayName': self.author1.get_display_name(),
            'id': author1Url,
            'host': author1Url.split("/author/")[0],
            'url': author1Url
        })

        response = self.client.get(get_pending_requests_path(str(self.author1.id)))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0], {
            'displayName': self.author3.get_display_name(),
            'id': author3Url,
            'host': author3Url.split("/author/")[0],
            'url': author3Url
        })

    def test_three_friend_requests_diff_users(self):
        author1Url = get_author_url(str(self.author1.id))
        author2Url = get_author_url(str(self.author2.id))
        author3Url = get_author_url(str(self.author3.id))

        FriendRequest.objects.create(requester=author1Url, friend=author2Url)
        FriendRequest.objects.create(requester=author3Url, friend=author1Url)
        FriendRequest.objects.create(requester=author2Url, friend=author3Url)

        response = self.client.get(get_pending_requests_path(str(self.author2.id)))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0], {
            'displayName': self.author1.get_display_name(),
            'id': author1Url,
            'host': author1Url.split("/author/")[0],
            'url': author1Url
        })

        response = self.client.get(get_pending_requests_path(str(self.author1.id)))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0], {
            'displayName': self.author3.get_display_name(),
            'id': author3Url,
            'host': author3Url.split("/author/")[0],
            'url': author3Url
        })

        response = self.client.get(get_pending_requests_path(str(self.author3.id)))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0], {
            'displayName': self.author2.get_display_name(),
            'id': author2Url,
            'host': author2Url.split("/author/")[0],
            'url': author2Url
        })

def get_respond_to_requests_path(userId):
    view = AuthorViewSet()
    view.basename = "author"
    view.request = None
    return view.reverse_action("friend_requests_respond", args=[userId])

def get_respond_to_request_body(author1, approve, query="friendResponse"):
    return json.dumps({
        "query": query,
        "friend": {
            "id": "http://127.0.0.1:8000/author/" + str(author1),
            "host": "http://127.0.0.1:8000",
            "displayName": "Some random name 2",
            "url": "http://127.0.0.1:8000/author/" + str(author1)
        },
        "approve": approve
    })

class RespondFriendRequestViewsTest(TestCase):

    def setUp(self):
        self.author1 = setupUser("one", "password")
        self.author2 = setupUser("two", "password")
        self.author3 = setupUser("three", "password")
        
        self.client.login(username="one", password="password")

    def test_unauthenticated(self):
        self.client.logout()
        author1Url = get_author_url(str(self.author1.id))
        author3Url = get_author_url(str(self.author3.id))
        FriendRequest.objects.create(requester=author3Url, friend=author1Url)

        body = get_respond_to_request_body(self.author3.id, False)
        response = self.client.post(get_respond_to_requests_path(str(self.author1.id)), data=body, content_type="application/json")
        self.assertEqual(response.status_code, 403)
        
    def test_authenticated_wrong_user(self):
        self.client.login(username="two", password="password")
        author1Url = get_author_url(str(self.author1.id))
        author3Url = get_author_url(str(self.author3.id))
        FriendRequest.objects.create(requester=author3Url, friend=author1Url)

        body = get_respond_to_request_body(self.author3.id, False)
        response = self.client.post(get_respond_to_requests_path(str(self.author1.id)), data=body, content_type="application/json")
        self.assertEqual(response.status_code, 403)
        
    def test_get(self):
        response = self.client.get(get_respond_to_requests_path(str(self.author1.id)))
        self.assertEqual(response.status_code, 405)

    def test_invalid_user(self):
        deletedId = self.author1.id
        self.author1.delete()
        body = get_respond_to_request_body(deletedId, True)
        response = self.client.post(get_respond_to_requests_path(str(deletedId)), data=body, content_type="application/json")
        self.assertEqual(response.status_code, 404)

    def test_invalid_query(self):
        body = get_respond_to_request_body(self.author1.id, True, "Not correct")
        response = self.client.post(get_respond_to_requests_path(str(self.author1.id)), data=body, content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_invalid_success(self):
        body = get_respond_to_request_body(self.author1.id, 25)
        response = self.client.post(get_respond_to_requests_path(str(self.author1.id)), data=body, content_type="application/json")
        self.assertEqual(response.status_code, 400)
    
    def test_no_request_from_friend(self):
        body = get_respond_to_request_body(self.author2.id, False)
        response = self.client.post(get_respond_to_requests_path(str(self.author1.id)), data=body, content_type="application/json")
        self.assertEqual(response.status_code, 404)

    def test_request_from_other_friend(self):
        author1Url = get_author_url(str(self.author1.id))
        author3Url = get_author_url(str(self.author3.id))
        FriendRequest.objects.create(requester=author3Url, friend=author1Url)

        body = get_respond_to_request_body(self.author2.id, False)
        response = self.client.post(get_respond_to_requests_path(str(self.author1.id)), data=body, content_type="application/json")
        self.assertEqual(response.status_code, 404)

    def test_successful_approve_response(self):
        author1Url = get_author_url(str(self.author1.id))
        author3Url = get_author_url(str(self.author3.id))
        FriendRequest.objects.create(requester=author3Url, friend=author1Url)

        body = get_respond_to_request_body(self.author3.id, True)
        response = self.client.post(get_respond_to_requests_path(str(self.author1.id)), data=body, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(FriendRequest.objects.all()), 0)
        self.assertIsNotNone(Follow.objects.get(follower=author1Url, followed=author3Url))

    def test_successful_reject_response(self):
        author1Url = get_author_url(str(self.author1.id))
        author3Url = get_author_url(str(self.author3.id))
        FriendRequest.objects.create(requester=author3Url, friend=author1Url)

        body = get_respond_to_request_body(self.author3.id, False)
        response = self.client.post(get_respond_to_requests_path(str(self.author1.id)), data=body, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(FriendRequest.objects.all()), 0)
        self.assertEqual(len(Follow.objects.all()), 0)

    def test_successful_reject_response_multiple_requests(self):
        author1Url = get_author_url(str(self.author1.id))
        author2Url = get_author_url(str(self.author2.id))
        author3Url = get_author_url(str(self.author3.id))
        FriendRequest.objects.create(requester=author2Url, friend=author1Url)
        FriendRequest.objects.create(requester=author3Url, friend=author1Url)

        body = get_respond_to_request_body(self.author3.id, False)
        response = self.client.post(get_respond_to_requests_path(str(self.author1.id)), data=body, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(FriendRequest.objects.all()), 1)
        self.assertIsNotNone(FriendRequest.objects.get(friend=author1Url, requester=author2Url))
        self.assertEqual(len(Follow.objects.all()), 0)

    def test_successful_approve_response_multiple_requests(self):
        author1Url = get_author_url(str(self.author1.id))
        author2Url = get_author_url(str(self.author2.id))
        author3Url = get_author_url(str(self.author3.id))
        FriendRequest.objects.create(requester=author2Url, friend=author1Url)
        FriendRequest.objects.create(requester=author3Url, friend=author1Url)

        body = get_respond_to_request_body(self.author3.id, True)
        response = self.client.post(get_respond_to_requests_path(str(self.author1.id)), data=body, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(FriendRequest.objects.all()), 1)
        self.assertIsNotNone(FriendRequest.objects.get(friend=author1Url, requester=author2Url))
        self.assertEqual(len(Follow.objects.all()), 1)
        self.assertIsNotNone(Follow.objects.get(follower=author1Url, followed=author3Url))