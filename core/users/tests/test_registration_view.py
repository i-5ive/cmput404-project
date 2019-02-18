from django.test import TestCase

from core.authors.models import Author
from core.users.models import User
from core.authors.tests.util import setupUser
from django.contrib.auth.hashers import check_password

# apparently django reverse doesn't want to work for this
USERS_PATH = "/users/"
EXISTING_USER = "yeet"
VALID_PASSWORD = "abcdefgh"
VALID_USERNAME = "new_account_username"

def get_body(username, password):
    return {
        "username": username,
        "password": password,
        "email": ""
    }

class RegisterUserTest(TestCase):

    def test_existing_user(self):
        setupUser(EXISTING_USER)
        body = get_body(EXISTING_USER, VALID_PASSWORD)
        response = self.client.post(USERS_PATH, data=body, content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(len(User.objects.all()), 1)

    def test_empty_username(self):
        body = get_body("", VALID_PASSWORD)
        response = self.client.post(USERS_PATH, data=body, content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(len(User.objects.all()), 0)

    def test_short_password(self):
        body = get_body(VALID_USERNAME, "")
        response = self.client.post(USERS_PATH, data=body, content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(len(User.objects.all()), 0)

    def test_long_username(self):
        body = get_body(VALID_USERNAME * 20, VALID_PASSWORD)
        response = self.client.post(USERS_PATH, data=body, content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(len(User.objects.all()), 0)

    def test_long_password(self):
        body = get_body(VALID_USERNAME, VALID_PASSWORD * 20)
        response = self.client.post(USERS_PATH, data=body, content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(len(User.objects.all()), 0)

    def test_success(self):
        body = get_body(VALID_USERNAME, VALID_PASSWORD)
        response = self.client.post(USERS_PATH, data=body, content_type="application/json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(len(User.objects.all()), 1)
        user = User.objects.get(username=VALID_USERNAME)
        self.assertTrue(check_password(VALID_PASSWORD, user.password))
        self.assertIsNotNone(Author.objects.get(user=user, approved=False))
