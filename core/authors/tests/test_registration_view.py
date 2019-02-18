from django.test import TestCase
from django.urls import reverse

from core.authors.models import Author
from core.users.models import User
from core.authors.registration_view import REGISTER
from core.authors.tests.util import setupUser

EXISTING_USER = "yeet"
VALID_PASSWORD = "abcdefgh"
VALID_USERNAME = "new account username"

def get_body(username, password, query=REGISTER):
    return {
        "query": query,
        "username": username,
        "password": password
    }

class RegisterUserTest(TestCase):

    def test_incorrect_query(self):
        body = get_body(VALID_USERNAME, VALID_PASSWORD, query="NotCorrect")
        response = self.client.post(reverse('register'), data=body, content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["query"], REGISTER)
        self.assertEqual(response.data["success"], False)
        self.assertIsNotNone(response.data["message"])
        self.assertEqual(len(User.objects.all()), 0)

    def test_existing_user(self):
        setupUser(EXISTING_USER)
        body = get_body(EXISTING_USER, VALID_PASSWORD)
        response = self.client.post(reverse('register'), data=body, content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["query"], REGISTER)
        self.assertEqual(response.data["success"], False)
        self.assertIsNotNone(response.data["message"])
        self.assertEqual(len(User.objects.all()), 1)

    def test_empty_username(self):
        body = get_body("", VALID_PASSWORD)
        response = self.client.post(reverse('register'), data=body, content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["query"], REGISTER)
        self.assertEqual(response.data["success"], False)
        self.assertIsNotNone(response.data["message"])
        self.assertEqual(len(User.objects.all()), 0)

    def test_short_password(self):
        body = get_body(VALID_USERNAME, "a")
        response = self.client.post(reverse('register'), data=body, content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["query"], REGISTER)
        self.assertEqual(response.data["success"], False)
        self.assertIsNotNone(response.data["message"])
        self.assertEqual(len(User.objects.all()), 0)

    def test_long_username(self):
        body = get_body(VALID_USERNAME * 20, VALID_PASSWORD)
        response = self.client.post(reverse('register'), data=body, content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["query"], REGISTER)
        self.assertEqual(response.data["success"], False)
        self.assertIsNotNone(response.data["message"])
        self.assertEqual(len(User.objects.all()), 0)

    def test_long_password(self):
        body = get_body(VALID_USERNAME, VALID_PASSWORD * 20)
        response = self.client.post(reverse('register'), data=body, content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["query"], REGISTER)
        self.assertEqual(response.data["success"], False)
        self.assertIsNotNone(response.data["message"])
        self.assertEqual(len(User.objects.all()), 0)

    def test_success(self):
        body = get_body(VALID_USERNAME, VALID_PASSWORD)
        response = self.client.post(reverse('register'), data=body, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["query"], REGISTER)
        self.assertEqual(response.data["success"], True)
        self.assertIsNotNone(response.data["message"])
        self.assertEqual(len(User.objects.all()), 1)

        user = User.objects.get(username=VALID_USERNAME, password=VALID_PASSWORD)
        self.assertIsNotNone(Author.objects.get(user=user, approved=False))
