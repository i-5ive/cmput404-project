from django.test import TestCase
from core.servers.SafeServerUtil import ServerUtil
from core.servers.models import Server

class PostViewsTest(TestCase):
    def test_server_user_is_server(self):
        server = Server.objects.create(base_url="https://hotstuff.com")
        
        self.assertTrue(ServerUtil.is_server(server))
        self.assertTrue(not ServerUtil.is_author(server))