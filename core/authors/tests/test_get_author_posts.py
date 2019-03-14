from django.test import TestCase

from core.authors.util import get_author_url

from core.authors.tests.util import setupUser, createPostForAuthor, makeFriends

from core.posts.models import Posts

class TestAuthorPost(TestCase):
    """
    /author/posts
    Tests
    """
    # Test we get only public posts when we do not authenticate
    def test_get_no_auth(self):
        author1 = setupUser("test_get_no_auth_user1")
        numPublicPosts = Posts.objects.all().filter(visibility__in=["PUBLIC","SERVERONLY"]).count()

        # Number of posts should be equal
        resp = self.client.get("/author/posts/").data
        self.assertEqual(numPublicPosts, resp["count"])

        # add a public post
        createPostForAuthor(author1, "test_get_no_auth author1's public post")

        # The number of public posts should have increased by one
        resp = self.client.get("/author/posts/").data
        self.assertEqual(numPublicPosts+1, resp["count"])

        # add a server-only post
        createPostForAuthor(author1, "test_get_no_auth author1's server-only post", "SERVERONLY")

        # The number of public posts should have increased by two now
        resp = self.client.get("/author/posts/").data
        self.assertEqual(numPublicPosts+2, resp["count"])

        # add a private post
        createPostForAuthor(author1, "test_get_no_auth author1's private post", "PRIVATE")
        # add a friends-only post
        createPostForAuthor(author1, "test_get_no_auth author1's friends-only post", "FRIENDS")
        # add a foaf-visible post
        createPostForAuthor(author1, "test_get_no_auth author1's foaf-only post", "FOAF")

        # The number of posts should have not increased since last time
        resp = self.client.get("/author/posts/").data
        self.assertEqual(numPublicPosts+2, resp["count"])

    # Test that we see friend's posts if we're authenticated
    def test_see_friend_posts(self):
        a1password = "guest"
        a1name = "test_see_friend_posts_user1"
        author1 = setupUser(a1name, a1password)
        author2 = setupUser("test_see_friend_posts_user2")
        
        self.client.login(username=a1name, password=a1password)
        
        numPublicPosts = Posts.objects.all().filter(visibility__in=["PUBLIC","SERVERONLY"]).count()
        resp = self.client.get("/author/posts/").data
        self.assertEqual(numPublicPosts, resp["count"]) # no friends yet, so nothing should be different

        # add a post by author 2
        createPostForAuthor(author2, "test_see_friend_posts user2's friends posts", "FRIENDS")

        resp = self.client.get("/author/posts/").data
        self.assertEqual(numPublicPosts, resp["count"]) # no friends yet, so nothing should be different

        makeFriends(author1, author2)

        # Should be an extra post returned because they're friends :)
        resp = self.client.get("/author/posts/").data
        self.assertEqual(numPublicPosts+1, resp["count"])

        self.client.logout()

    # Test FOAF-ness of posts
    # A is friend of B can see FOAFs and Friends
    # A is FOAF of C can see FOAFs (but not Friends)
    # A is 3-rd degree friend of D, cannot see FOAFs or Friends
    def test_foafing_posts(self):
        a1password = "guest"
        a1name = "test_foafing_posts_user1"
        A = setupUser(a1name, a1password)
        B = setupUser("test_foafing_posts_user2")
        C = setupUser("test_foafing_posts_user3")
        D = setupUser("test_foafing_posts_user4")

        self.client.login(username=a1name, password=a1password) # login to user A
        numPublicPosts = Posts.objects.all().filter(visibility__in=["PUBLIC","SERVERONLY"]).count()

        # Add a FOAF post for B
        createPostForAuthor(B, "a FOAF post from user B", "FOAF")
        # Add a FOAF post for C
        createPostForAuthor(C, "a FOAF post from user C", "FOAF")
        # Add a FOAF post for D
        createPostForAuthor(D, "a FOAF post from user D", "FOAF")

        resp = self.client.get("/author/posts/").data
        self.assertEqual(numPublicPosts, resp["count"]) # no friends yet, so nothing should be different

        makeFriends(A, B)
        resp = self.client.get("/author/posts/").data
        self.assertEqual(numPublicPosts+1, resp["count"]) # we should see B's 1 FOAF post

        makeFriends(B, C)
        resp = self.client.get("/author/posts/").data
        self.assertEqual(numPublicPosts+2, resp["count"]) # we should see C's 1 FOAF post

        makeFriends(C, D)
        resp = self.client.get("/author/posts/").data
        self.assertEqual(numPublicPosts+2, resp["count"]) # we shouldn't see third degree posts (# stays the same last time)

        # Add a Friends post for C
        createPostForAuthor(C, "a FRIENDS post from user C", "FRIENDS")
        resp = self.client.get("/author/posts/").data
        self.assertEqual(numPublicPosts+2, resp["count"]) # we shouldn't see FOAF Friend posts (# stays the same last time)

        self.client.logout()

    # user should be able to see their own posts
    def test_see_own(self):
        aName = "test_see_own_user"
        aPassword = "guest"
        author = setupUser(aName, aPassword)
        numPublicPosts = Posts.objects.all().filter(visibility__in=["PUBLIC","SERVERONLY"]).count()

        self.client.login(username=aName, password=aPassword) # login to the user

        # Number of posts should be equal
        resp = self.client.get("/author/posts/").data
        self.assertEqual(numPublicPosts, resp["count"])

        # add a public post (increases post count by one)
        createPostForAuthor(author, "test_see_own_user author's public post", "PUBLIC")
        resp = self.client.get("/author/posts/").data
        self.assertEqual(numPublicPosts+1, resp["count"])

        # add a private post (increases post count by one)
        createPostForAuthor(author, "test_see_own_user author's private post", "PRIVATE")
        resp = self.client.get("/author/posts/").data
        self.assertEqual(numPublicPosts+2, resp["count"])

        # add a server-only post (increases post count by one)
        createPostForAuthor(author, "test_see_own_user author's server-only post", "SERVERONLY")
        resp = self.client.get("/author/posts/").data
        self.assertEqual(numPublicPosts+3, resp["count"])

        # add a friends post (increases post count by one)
        createPostForAuthor(author, "test_see_own_user author's friends post", "FRIENDS")
        resp = self.client.get("/author/posts/").data
        self.assertEqual(numPublicPosts+4, resp["count"])

        # add a foaf post (increases post count by one)
        createPostForAuthor(author, "test_see_own_user author's foaf post", "FOAF")
        resp = self.client.get("/author/posts/").data
        self.assertEqual(numPublicPosts+5, resp["count"])

        self.client.logout()

    # Can a user see a post they are allowed to?
    def test_see_private(self):
        aName = "test_see_private_user"
        aPassword = "guest"
        author1 = setupUser(aName, aPassword)
        author2 = setupUser("test_see_private_user2")
        self.client.login(username=aName, password=aPassword) # login to the first author

        numPublicPosts = Posts.objects.all().filter(visibility__in=["PUBLIC","SERVERONLY"]).count()

        # Number of posts should be equal
        resp = self.client.get("/author/posts/").data
        self.assertEqual(numPublicPosts, resp["count"])

        # add a private post that author 1 is allowed to see
        createPostForAuthor(author2, "test_see_own_user author's public post", "PUBLIC", [get_author_url(str(author1.pk))])
        resp = self.client.get("/author/posts/").data
        self.assertEqual(numPublicPosts+1, resp["count"])

        self.client.logout()

    """
    /author/{id}/posts
    Tests
    """