from django.test import TestCase

from core.authors.util import get_author_url

from core.authors.tests.util import setupUser, createPostForAuthor, makeFriends

from core.posts.models import Posts

def getAuthorPostUrl(author):
    return "/author/" + str(author.pk) + "/posts/"

class TestAuthorPost(TestCase):
    """
    /author/posts
    Tests
    """
    # Test we get only public posts when we do not authenticate
    def test_get_no_auth(self):
        author1 = setupUser("test_get_no_auth_user1")
        numPublicPosts = Posts.objects.all().filter(visibility__in=["PUBLIC"]).count()

        # Number of posts should be equal
        resp = self.client.get("/author/posts/").data
        self.assertEqual(numPublicPosts, resp["count"])

        # add a public post
        createPostForAuthor(author1, "test_get_no_auth author1's public post")

        # The number of public posts should have increased by one
        resp = self.client.get("/author/posts/").data
        self.assertEqual(numPublicPosts+1, resp["count"])

        # add a server-only post which do not show 
        createPostForAuthor(author1, "test_get_no_auth author1's server-only post", "SERVERONLY")

        # The number of public posts should have increased by one only
        resp = self.client.get("/author/posts/").data
        self.assertEqual(numPublicPosts+1, resp["count"])

        # add a private post
        createPostForAuthor(author1, "test_get_no_auth author1's private post", "PRIVATE")
        # add a friends-only post
        createPostForAuthor(author1, "test_get_no_auth author1's friends-only post", "FRIENDS")
        # add a foaf-visible post
        createPostForAuthor(author1, "test_get_no_auth author1's foaf-only post", "FOAF")

        # The number of posts should have not increased since last time
        resp = self.client.get("/author/posts/").data
        self.assertEqual(numPublicPosts+1, resp["count"])

    # Test that we see friend's posts if we're authenticated
    def test_see_friend_posts(self):
        a1password = "guest"
        a1name = "test_see_friend_posts_user1"
        author1 = setupUser(a1name, a1password)
        author2 = setupUser("test_see_friend_posts_user2")
        
        self.client.login(username=a1name, password=a1password)
        
        numPublicPosts = Posts.objects.all().filter(visibility__in=["PUBLIC"]).count()
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
        numPublicPosts = Posts.objects.all().filter(visibility__in=["PUBLIC"]).count()

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
        numPublicPosts = Posts.objects.all().filter(visibility__in=["PUBLIC"]).count()

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

    # unlisted posts should not show up in any query
    def test_unlisted(self):
        aName = "test_unlisted_user"
        aPassword = "guest"
        author = setupUser("test_unlisted_user2")
        author2 = setupUser(aName, aPassword)

        numPublicPosts = Posts.objects.all().filter(visibility__in=["PUBLIC","SERVERONLY"]).count()

        createPostForAuthor(author, "public content", "PUBLIC", unlisted=True)
        createPostForAuthor(author, "server content", "SERVERONLY", unlisted=True)
        createPostForAuthor(author, "friend content", "FRIENDS", unlisted=True)
        createPostForAuthor(author, "foaf content", "FOAF", unlisted=True)
        createPostForAuthor(author, "private content", "PRIVATE", unlisted=True)
        createPostForAuthor(author2, "public content", "PUBLIC", unlisted=True)
        createPostForAuthor(author2, "server content", "SERVERONLY", unlisted=True)
        createPostForAuthor(author2, "friend content", "FRIENDS", unlisted=True)
        createPostForAuthor(author2, "foaf content", "FOAF", unlisted=True)
        createPostForAuthor(author2, "private content", "PRIVATE", unlisted=True)
        
        resp = self.client.get("/author/posts/").data
        for post in resp["posts"]:
            print(post)
        self.assertEqual(numPublicPosts, resp["count"]) # nothing should have changed (all unlisted)

        self.client.login(username=aName, password=aPassword)

        resp = self.client.get("/author/posts/").data
        self.assertEqual(numPublicPosts, resp["count"]) # nothing should have changed (all unlisted)

        # check if making friends changes anything
        makeFriends(author,author2)

        resp = self.client.get("/author/posts/").data
        self.assertEqual(numPublicPosts, resp["count"]) # nothing should have changed (all unlisted)

        self.client.logout()

    """ " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " "
    /author/{id}/posts
    Tests
    " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " """
    def test_get_anon_for_author(self):
        author = setupUser("get_public_posts_for_author_user")
        url = getAuthorPostUrl(author)

        # No posts yet, new author
        resp = self.client.get(url).data
        self.assertEqual(0, len(resp["posts"]))
        self.assertEqual(0, resp["count"])

        # add a public post
        createPostForAuthor(author, "test_get_anon_for_author public post")

        # public posts should be visible
        resp = self.client.get(url).data
        self.assertEqual(1, len(resp["posts"]))
        self.assertEqual(1, resp["count"])

        # add a private post
        createPostForAuthor(author, "test_get_no_auth author1's private post", "PRIVATE")
        # add a friends-only post
        createPostForAuthor(author, "test_get_no_auth author1's friends-only post", "FRIENDS")
        # add a foaf-visible post
        createPostForAuthor(author, "test_get_no_auth author1's foaf-only post", "FOAF")

        # num posts should not have changed (1)
        resp = self.client.get(url).data
        self.assertEqual(1, len(resp["posts"]))
        self.assertEqual(1, resp["count"])

        # server-only posts do not increase the amount visible
        createPostForAuthor(author, "test_get_anon_for_author public post", "SERVERONLY")

        # should return 2 posts now
        resp = self.client.get(url).data
        self.assertEqual(1, len(resp["posts"]))
        self.assertEqual(1, resp["count"])

    def test_get_author_unlisted(self):
        author = setupUser("test_get_author_unlisted_user")
        aName = "test_get_author_unlisted_user2"
        aPassword = "guest"
        author2 = setupUser(aName, aPassword)
        url = getAuthorPostUrl(author)

        # all posts are unlisted
        createPostForAuthor(author, "public content", "PUBLIC", unlisted=True)
        createPostForAuthor(author, "server content", "SERVERONLY", unlisted=True)
        createPostForAuthor(author, "friend content", "FRIENDS", unlisted=True)
        createPostForAuthor(author, "foaf content", "FOAF", unlisted=True)
        createPostForAuthor(author, "private content", "PRIVATE", unlisted=True)

        # none of the posts should be visible (anon)
        resp = self.client.get(url).data
        self.assertEqual(0, resp["count"])

        self.client.login(username=aName, password=aPassword)

        # none of the posts should be visible (logged in)
        resp = self.client.get(url).data
        self.assertEqual(0, resp["count"])

        makeFriends(author, author2)

        # none of the posts should be visible (regardless of friendship)
        resp = self.client.get(url).data
        self.assertEqual(0, resp["count"])

    def test_author_friend(self):
        author = setupUser("test_author_friend_user")
        aName = "test_author_friend_user2"
        aPassword = "guest"
        author2 = setupUser(aName, aPassword)
        url = getAuthorPostUrl(author)
        self.client.login(username=aName, password=aPassword)

        createPostForAuthor(author, "friend content", "FRIENDS")
        createPostForAuthor(author, "foaf content", "FOAF")
        createPostForAuthor(author, "private content", "PRIVATE")

        # none of the posts should be visible (they aren't friends yet)
        resp = self.client.get(url).data
        self.assertEqual(0, resp["count"])

        makeFriends(author, author2)

        # two posts (foaf, friends) should be visible (they're friends now)
        resp = self.client.get(url).data
        self.assertEqual(2, resp["count"])

    # test that foaf returns their foaf posts
    def test_author_foaf(self):
        author = setupUser("test_author_foaf_user")
        aName = "test_author_foaf_user2"
        aPassword = "guest"
        author2 = setupUser(aName, aPassword)
        middleAuthor = setupUser("middleman_test_author_foaf")
        url = getAuthorPostUrl(author)
        self.client.login(username=aName, password=aPassword)

        createPostForAuthor(author, "friend content", "FRIENDS")
        createPostForAuthor(author, "foaf content", "FOAF")
        createPostForAuthor(author, "private content", "PRIVATE")

        # none of the posts should be visible (they aren't foafs yet)
        resp = self.client.get(url).data
        self.assertEqual(0, resp["count"])

        makeFriends(middleAuthor, author2)
        makeFriends(middleAuthor, author)

        # only the foaf post should be visible
        resp = self.client.get(url).data
        self.assertEqual(1, resp["count"])

    def test_author_private(self):
        author = setupUser("test_author_foaf_user")
        aName = "test_author_foaf_user2"
        aPassword = "guest"
        author2 = setupUser(aName, aPassword)
        middleAuthor = setupUser("middleman_test_author_foaf")
        url = getAuthorPostUrl(author)
        self.client.login(username=aName, password=aPassword)

        createPostForAuthor(author, "friend content", "FRIENDS")
        createPostForAuthor(author, "foaf content", "FOAF")
        createPostForAuthor(author, "private content", "PRIVATE")
        createPostForAuthor(author, "probably noodz", "PRIVATE", makeVisibleTo=[get_author_url(str(author2.pk))])

        # only the visibleTo post should be visible
        resp = self.client.get(url).data
        self.assertEqual(1, resp["count"])

    # Make sure other posts don't slip in
    def test_author_only(self):
        author = setupUser("test_author_only")
        aName = "test_author_only_reader"
        aPassword = "guest"
        reader = setupUser(aName, aPassword)
        url = getAuthorPostUrl(author)
        noisemaker1 = setupUser("noisy1")
        noisemaker2 = setupUser("noisy2")
        noisemaker3 = setupUser("noisy3")
        createPostForAuthor(noisemaker1, "here's a public post")
        createPostForAuthor(noisemaker1, "I ate mac and cheese for lunch")
        createPostForAuthor(noisemaker1, "I love my mom")
        createPostForAuthor(noisemaker1, "I love my friends more, sorry mom", "FRIENDS")
        createPostForAuthor(noisemaker2, "Why would anyone try to tackle Twitter and Mastodon?")
        createPostForAuthor(noisemaker3, "@noisy2, I think this is a school project")
        createPostForAuthor(noisemaker2, "Am I even real then?")
        createPostForAuthor(noisemaker2, "Dear Diary, I'm having an existential crisis...", "PRIVATE")
        createPostForAuthor(noisemaker3, "If you have no friends, this post is the same as a private one :)", "FRIENDS")
        createPostForAuthor(noisemaker1, "@noisy3 do you like my mac and cheese?")
        createPostForAuthor(reader, "I enjoy reading but I also enjoy posting")
        createPostForAuthor(noisemaker2, "Can you review my new book 'Getting Out of Here', I'll send you an email with it.", "PRIVATE", makeVisibleTo=[get_author_url(str(reader.pk))])
        createPostForAuthor(reader, "@noisy2 Sorry, I can't read your book, it's just frantic scribbling.")
        createPostForAuthor(noisemaker2, "@test_author_only_reader DON'T TELL THEM HERE")
        self.client.login(username=aName, password=aPassword)

        # the author we are tracking hasn't made any posts
        resp = self.client.get(url).data
        self.assertEqual(0, resp["count"])

        makeFriends(author, noisemaker1)
        makeFriends(author, noisemaker2)
        makeFriends(noisemaker3, noisemaker2)
        makeFriends(noisemaker3, reader)
        makeFriends(author, reader)

        # the author we are tracking hasn't made any posts
        resp = self.client.get(url).data
        self.assertEqual(0, resp["count"])

        createPostForAuthor(author, "Hello I read your book and I have some questions", "PRIVATE", makeVisibleTo=[get_author_url(str(noisemaker2.pk))])
        createPostForAuthor(author, "this is kind of meta since my variable name is also author", "PRIVATE")

        # the author we are tracking hasn't made any (public) posts
        resp = self.client.get(url).data
        self.assertEqual(0, resp["count"])
