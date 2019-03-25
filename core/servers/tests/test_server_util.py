from django.test import TestCase
from core.servers.SafeServerUtil import ServerUtil
from core.servers.models import Server

class PostViewsTest(TestCase):
    def test_(self):
        self.client.login(username="user2", password="password")
        