from django.test import TestCase
from core.servers.SafeServerUtil import ServerUtil
from core.servers.models import Server
from core.authors.models import Author
from core.users.models import User

class PostViewsTest(TestCase):
    def test_server_user_is_server(self):
        user = User.objects.create()
        server = Server.objects.create(user=user, base_url="https://hotstuff.com")
        
        self.assertTrue(ServerUtil.is_server(server), "server should be server")
        self.assertTrue(not ServerUtil.is_author(server), "server is not author")

    def test_author_is_author(self):
        user = User.objects.create()
        author = Author.objects.create(user=user)
        
        self.assertTrue(not ServerUtil.is_server(author), "author is not server")
        self.assertTrue(ServerUtil.is_author(author), "author should be author")