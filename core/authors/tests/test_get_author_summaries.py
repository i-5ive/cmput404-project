import requests
import json

from django.test import TestCase

from core.authors.models import Author
from core.authors.util import get_author_summaries, get_author_url
from core.authors.tests.util import setupUser
from core.hostUtil import get_host_url

import unittest
from unittest.mock import patch

MOCK_HOST = get_host_url()
EXTERNAL_HOST_ONE = "http://192.168.0.1"
EXTERNAL_HOST_TWO = "http://softwareprocess.es"

def _setupAuthor(name):
    author = setupUser(name)
    author.displayName = name
    author.save()
    return str(author.id)

class MockRequestsPost:
    def __init__(self, content):
        self.content = content

class TestGetAuthorSummaries(TestCase):

    def setUp(self):
        self.author1 = _setupAuthor("a")
        self.author2 = _setupAuthor("b")
        self.author3 = _setupAuthor("c")

    def test_empty_call(self):
        self.assertEqual(len(get_author_summaries([])), 0)

    @patch("core.hostUtil.get_host_url")
    def test_only_local(self, url_mock):
        url_mock.return_value = MOCK_HOST

        urls = [get_author_url(self.author1), get_author_url(self.author2)]
        summaries = get_author_summaries(urls)
        summaries.sort(key=lambda x : x["displayName"])
        self.assertEqual(summaries, [{
            "host": MOCK_HOST,
            "id": get_author_url(self.author1),
            "url": get_author_url(self.author1),
            "displayName": "a"
        }, {
            "host": MOCK_HOST,
            "id": get_author_url(self.author2),
            "url": get_author_url(self.author2),
            "displayName": "b"
        }])
    
    # @patch("requests.post")
    # @patch("core.hostUtil.get_host_url")
    # def test_one_external_host(self, url_mock, requests_mock):
    #     url_mock.return_value = MOCK_HOST

    #     author1 = EXTERNAL_HOST_ONE + "/author/" + self.author1
    #     author2 = EXTERNAL_HOST_ONE + "/author/" + self.author2
    #     expectedSummaries = [{
    #         "host": EXTERNAL_HOST_ONE,
    #         "id": author1,
    #         "url": author1,
    #         "displayName": "a"
    #     }, {
    #         "host": EXTERNAL_HOST_ONE,
    #         "id": author2,
    #         "url": author2,
    #         "displayName": "b"
    #     }]
    #     requests_return = MockRequestsPost(json.dumps(expectedSummaries))
    #     requests_mock.return_value = requests_return

    #     urls = [author1, author2]
    #     summaries = get_author_summaries(urls)

    #     requests_mock.assert_called_once_with(EXTERNAL_HOST_ONE + "/authorSummaries", data=json.dumps(urls), headers={"Content-Type": "application/json"})
    #     self.assertEqual(summaries, expectedSummaries)

    # @patch("requests.post")
    # @patch("core.hostUtil.get_host_url")
    # def test_multiple_external_hosts(self, url_mock, requests_mock):
    #     url_mock.return_value = MOCK_HOST

    #     author1 = EXTERNAL_HOST_ONE + "/author/" + self.author1
    #     author2 = EXTERNAL_HOST_TWO + "/author/" + self.author2
    #     author1Summary = {
    #         "host": EXTERNAL_HOST_ONE,
    #         "id": author1,
    #         "url": author1,
    #         "displayName": "a"
    #     }
    #     author2Summary = {
    #         "host": EXTERNAL_HOST_TWO,
    #         "id": author2,
    #         "url": author2,
    #         "displayName": "b"
    #     }

    #     host_one_return = MockRequestsPost(json.dumps([author1Summary]))
    #     host_two_return = MockRequestsPost(json.dumps([author2Summary]))
    #     requests_mock.side_effect = lambda host, data, headers : (host_one_return if EXTERNAL_HOST_ONE in host else host_two_return)

    #     urls = [author1, author2]
    #     summaries = get_author_summaries(urls)

    #     requests_mock.assert_any_call(EXTERNAL_HOST_ONE + "/authorSummaries", data=json.dumps([author1]), headers={"Content-Type": "application/json"})
    #     requests_mock.assert_any_call(EXTERNAL_HOST_TWO + "/authorSummaries", data=json.dumps([author2]), headers={"Content-Type": "application/json"})
    #     self.maxDiff = None
    #     self.assertEqual(sorted(summaries, key=lambda x : x["displayName"]), sorted([author1Summary, author2Summary], key=lambda x : x["displayName"]))

    # @patch("requests.post")
    # @patch("core.hostUtil.get_host_url")
    # def test_external_and_local(self, url_mock, requests_mock):
    #     url_mock.return_value = MOCK_HOST

    #     author1 = EXTERNAL_HOST_ONE + "/author/" + self.author1
    #     author2 = EXTERNAL_HOST_TWO + "/author/" + self.author2
    #     author3 = get_author_url(self.author3)

    #     author1Summary = {
    #         "host": EXTERNAL_HOST_ONE,
    #         "id": author1,
    #         "url": author1,
    #         "displayName": "a"
    #     }
    #     author2Summary = {
    #         "host": EXTERNAL_HOST_TWO,
    #         "id": author2,
    #         "url": author2,
    #         "displayName": "b"
    #     }
    #     author3Summary = {
    #         "host": MOCK_HOST,
    #         "id": author3,
    #         "url": author3,
    #         "displayName": "c"
    #     }

    #     host_one_return = MockRequestsPost(json.dumps([author1Summary]))
    #     host_two_return = MockRequestsPost(json.dumps([author2Summary]))
    #     requests_mock.side_effect = lambda host, data, headers : (host_one_return if EXTERNAL_HOST_ONE in host else host_two_return)

    #     urls = [author1, author2, author3]
    #     summaries = get_author_summaries(urls)

    #     requests_mock.assert_any_call(EXTERNAL_HOST_ONE + "/authorSummaries", data=json.dumps([author1]), headers={"Content-Type": "application/json"})
    #     requests_mock.assert_any_call(EXTERNAL_HOST_TWO + "/authorSummaries", data=json.dumps([author2]), headers={"Content-Type": "application/json"})
    #     self.assertEqual(sorted(summaries, key=lambda x : x["displayName"]), sorted([author3Summary, author1Summary, author2Summary], key=lambda x : x["displayName"]))