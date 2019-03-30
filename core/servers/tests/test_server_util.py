from django.test import TestCase
from core.servers.SafeServerUtil import ServerUtil
from core.servers.models import Server
from core.authors.models import Author
from core.users.models import User

class PostViewsTest(TestCase):
    def test_server_user_is_server(self):
        user = User.objects.create(username="server-name")
        server = Server.objects.create(user=user, base_url="https://hotstuff.com")

        self.assertTrue(ServerUtil.is_server(user), "server should be server")
        self.assertTrue(not ServerUtil.is_author(user), "server is not author")

    def test_author_is_author(self):
        user = User.objects.create(username="author-name")
        # PITA Point: For SoMe ReAsOn CrEaTiNg A UsEr CrEaTeS An aUthOr
        #author = Author.objects.create(user=user)
        
        self.assertTrue(not ServerUtil.is_server(user), "author is not server")
        self.assertTrue(ServerUtil.is_author(user), "author should be author")