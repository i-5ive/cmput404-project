from django.test import TestCase

from core.authors.models import Author
from core.authors.views import AuthorViewSet

from core.authors.tests.util import setupUser

def get_request_body(displayName, firstName, lastName, email, github, bio):
    return {
        "displayName": displayName,
        "firstName": firstName,
        "lastName": lastName,
        "email": email,
        "github": github,
        "bio": bio
    }

def get_path(userId):
    view = AuthorViewSet()
    view.basename = "author"
    view.request = None
    return view.reverse_action("update", args=[userId])

class UpdateProfileTests(TestCase):

    def setUp(self):
        self.author1 = setupUser("one", "two")
        self.client.login(username="one", password="two")

    def test_get(self):
        response = self.client.get(get_path(str(self.author1.id)))
        self.assertEqual(response.status_code, 405)

    def test_unauthenticated(self):
        self.client.logout()
        body = get_request_body("abc", "a", "b", "x@y.com", "https://github.com/username", "abcd")
        response = self.client.post(get_path(str(self.author1.id)), body, type="json")
        self.assertEqual(response.status_code, 403)
        
    def test_unauthenticated_diff_user(self):
        setupUser("two", "password")
        self.client.login(username="two", password="password")
        body = get_request_body("abc", "a", "b", "x@y.com", "https://github.com/username", "abcd")
        response = self.client.post(get_path(str(self.author1.id)), body, type="json")
        self.assertEqual(response.status_code, 403)
        
    def test_invalid_user(self):
        deletedId = self.author1.id
        self.author1.delete()
        body = get_request_body("abc", "a", "b", "x@y.com", "", "abc")
        response = self.client.post(get_path(str(deletedId)), body, type="json")
        self.assertEqual(response.status_code, 404)

    def test_invalid_github(self):
        body = get_request_body("abc", "a", "b", "x@y.com", "https://gitgud.com/username", "abc")
        response = self.client.post(get_path(str(self.author1.id)), body, type="json")
        self.assertEqual(response.status_code, 400)

    def test_invalid_email(self):
        body = get_request_body("abc", "a", "b", "xy.com", "", "abc")
        response = self.client.post(get_path(str(self.author1.id)), body, type="json")
        self.assertEqual(response.status_code, 400)

    def test_bio_too_long(self):
        body = get_request_body("abc", "a", "b", "x@y.com", "", "abc" * 400)
        response = self.client.post(get_path(str(self.author1.id)), body, type="json")
        self.assertEqual(response.status_code, 400)

    def test_display_name_too_long(self):
        body = get_request_body("abcd" * 21, "a", "b", "x@y.com", "", "abc")
        response = self.client.post(get_path(str(self.author1.id)), body, type="json")
        self.assertEqual(response.status_code, 400)

    def test_first_name_too_long(self):
        body = get_request_body("abc", "a" * 100, "b", "x@y.com", "", "abc")
        response = self.client.post(get_path(str(self.author1.id)), body, type="json")
        self.assertEqual(response.status_code, 400)

    def test_successful_update(self):
        body = get_request_body("abc", "a", "b", "x@y.com", "https://github.com/username", "abcd")
        response = self.client.post(get_path(str(self.author1.id)), body, type="json")
        self.assertEqual(response.status_code, 200)
        self.author1 = Author.objects.get(pk=self.author1.id)
        self.assertEqual(self.author1.displayName, "abc")
        self.assertEqual(self.author1.user.first_name, "a")
        self.assertEqual(self.author1.user.last_name, "b")
        self.assertEqual(self.author1.user.email, "x@y.com")
        self.assertEqual(self.author1.github, "https://github.com/username")
        self.assertEqual(self.author1.bio, "abcd")

    def test_successful_update_no_github(self):
        body = get_request_body("abc", "a", "b", "x@y.com", "", "abcd")
        response = self.client.post(get_path(str(self.author1.id)), body, type="json")
        self.assertEqual(response.status_code, 200)
        self.author1 = Author.objects.get(pk=self.author1.id)
        self.assertEqual(self.author1.displayName, "abc")
        self.assertEqual(self.author1.user.first_name, "a")
        self.assertEqual(self.author1.user.last_name, "b")
        self.assertEqual(self.author1.user.email, "x@y.com")
        self.assertEqual(self.author1.github, "")
        self.assertEqual(self.author1.bio, "abcd")