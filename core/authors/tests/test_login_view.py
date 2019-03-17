from django.test import TestCase
from django.urls import reverse

from core.authors.models import Author
from core.users.models import User
from core.authors.tests.util import setupUser
from django.contrib.auth.hashers import check_password
from core.authors.login_view import QUERY

VALID_PASSWORD = "abcdefgh"
VALID_USERNAME = "new_account_username"
VALID_USERNAME_UNAPPROVED = "unapproved_account"

def get_body(username, password, query=QUERY):
    return {
        "username": username,
        "password": password,
        "query": query
    }

class LoginTest(TestCase):

    def setUp(self):
        self.user = setupUser(VALID_USERNAME, password=VALID_PASSWORD)
    
    def test_get(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 405)

    def test_wrong_query(self):
        body = get_body(VALID_USERNAME * 20, VALID_PASSWORD, "notlogin")
        response = self.client.post(reverse('login'), data=body, content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_invalid_username(self):
        body = get_body(VALID_USERNAME + "a", VALID_PASSWORD)
        response = self.client.post(reverse('login'), data=body, content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_invalid_password(self):
        body = get_body(VALID_USERNAME, VALID_PASSWORD + "a")
        response = self.client.post(reverse('login'), data=body, content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_unapproved_account(self):
        setupUser(VALID_USERNAME_UNAPPROVED)
        body = get_body(VALID_USERNAME_UNAPPROVED, VALID_PASSWORD)
        response = self.client.post(reverse('login'), data=body, content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_success(self):
        body = get_body(VALID_USERNAME, VALID_PASSWORD)
        response = self.client.post(reverse('login'), data=body, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["userId"], str(self.user.id))
