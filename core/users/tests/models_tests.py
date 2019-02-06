from django.test import TestCase

from core.users.models import Author


class AuthorModelTest(TestCase):

    def setUp(self):
        pass

    def test_create_author(self):
        old_count = Author.objects.count()
        author = Author.objects.create(**{
            'username': 'test123',
            'password': Author.objects.make_random_password(),
            'displayName': 'Test User'
        })
        self.assertIsNotNone(author)
        self.assertGreaterEqual(Author.objects.count(), old_count + 1, 'Incorrect number of users')
        self.assertEqual(author.get_username(), 'test123')
        self.assertEqual(author.get_display_name(), 'Test User')
