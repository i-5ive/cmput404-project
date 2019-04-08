import coreapi
from django.core.paginator import Paginator
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.schemas import AutoSchema

from core.authors.external_author_posts_view import get_external_author_posts
from core.authors.friend_request_view import get_author_details
from core.authors.friends_util import get_friends, get_friends_from_pk
from core.authors.friends_view import handle_friends_get, handle_friends_post
from core.authors.models import Author, Follow, FriendRequest
from core.authors.serializers import AuthorSerializer
from core.authors.util import get_author_url, get_author_summaries, get_author_id
from core.github_util import get_github_activity
from core.hostUtil import get_host_url, is_encoded_external_host
from core.posts.constants import DEFAULT_POST_PAGE_SIZE
from core.posts.models import Posts
from core.posts.serializers import PostsSerializer
from core.posts.util import add_page_details_to_response, merge_posts_with_github_activity
from core.servers.SafeServerUtil import ServerUtil


def validate_friend_request_response(body, pk):
    success = True
    message = "Your response has been recorded"
    friend_request = None
    friend_data = None

    if body["query"] != "friendResponse":
        success = False
        message = "The query value was not correct"
    elif not isinstance(body["approve"], bool):
        success = False
        message = "The approve value was not a boolean"
    else:
        friend_data = get_author_details(body["friend"])
        friend_request = FriendRequest.objects.filter(requester=friend_data["id"], friend=get_author_url(pk))

    return (success, message, friend_request, friend_data)


class AuthorViewSet(viewsets.ModelViewSet):
    """
    retrieve:
    Get a specific authorgi

    get_external_profile:
    Get an external author profile

    visible_posts:
    return a list of all posts visible to the authenticated user
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

    def retrieve(self, request, pk):
        try:
            author = Author.objects.get(pk=pk)
        except:
            print("DID WE GET HERE?", pk)
            return Response("Invalid author ID specified", status=404)

        url = get_author_url(pk)
        data = {
            "id": url,
            "host": get_host_url(),
            "displayName": author.displayName or author.user.username,
            "url": url,
            "friends": get_author_summaries(get_friends(url))
        }
        if (author.github):
            data["github"] = author.github
        if (author.user.first_name):
            data["firstName"] = author.user.first_name
        if (author.user.last_name):
            data["lastName"] = author.user.last_name
        if (author.user.email):
            data["email"] = author.user.email
        if (author.bio):
            data["bio"] = author.bio
        return Response(data)

    # author/external?authorUrl={value}
    # attempts to get an external author's profile
    @action(methods=['get'], detail=False, url_path="external")
    def get_external_profile(self, request):
        authorUrl = request.query_params.get("authorUrl", None)
        if not request.user.is_authenticated:
            return Response("You must be authenticated to use this endpoint.", status=403)
        if not authorUrl:
            return Response("You must specify an authorUrl query to use this endpoint", status=400)

        server = ServerUtil(authorUrl=authorUrl)
        if not server.is_valid():
            return Response("Could not find an external server in our database for the author url: " + authorUrl,
                            status=404)
        success, profile = server.get_author_info(authorUrl.split("author/")[1])
        if not success:
            return Response("Failed to connect with external server: " + server.get_base_url(), status=500)
        # for some reason we throw friends in here
        if "friends" not in profile:
            profile['friends'] = []
            server2 = ServerUtil(url=authorUrl.split('/author')[0])
            if server2.is_valid():
                success, friends = server2.get_author_friends(authorUrl.split("author/")[1])
                if success:
                    for friend in friends:
                        friend_server = ServerUtil(authorUrl=friend)
                        friend_id = friend.split('author/')[1]
                        if friend_server.is_valid():
                            success, info = friend_server.get_author_info(friend_id)
                            if success and info:
                                profile['friends'].append(info)

        return Response(profile)

    @action(methods=['get'], detail=True, url_path='friendrequests', url_name='friend_requests')
    def get_friend_requests(self, request, pk):
        try:
            author = Author.objects.get(pk=pk)
        except:
            return Response("Invalid author ID specified", status=404)

        requests = FriendRequest.objects.filter(friend=get_author_url(pk))
        print("requests found", len(requests))
        urls = []
        for pending_request in requests:
            urls.append(pending_request.requester)
        formatted_requests = get_author_summaries(urls)
        return Response(formatted_requests, status=200)

    # For inexplicable reasons, we have another endpoint for doing what serv/friendrequests
    # already does :) and we have to do extra work to get the data serv/friendrequests would
    # already have as well
    # A external server will never call this so we don't have to worry
    @action(methods=['post'], detail=True, url_path='friendrequests/respond', url_name='friend_requests_respond')
    def handle_friend_request_response(self, request, pk):
        try:
            author = Author.objects.get(pk=pk)
            if ((not request.user.is_authenticated) or request.user.author != author):
                return Response({
                    "query": "friendrequest",
                    "success": False,
                    "message": "You must be authenticated as the requested user to perform this action."
                }, status=status.HTTP_403_FORBIDDEN)
        except:
            return Response({
                "query": "friendrequest",
                "success": False,
                "message": "Invalid author ID specified"
            }, status=404)

        try:
            message = "The request body could not be parsed"
            body = request.data
            success, message, friend_request, friend_data = validate_friend_request_response(body, pk)
        except:
            return Response({
                "query": "friendrequest",
                "success": False,
                "message": message
            }, status=400)

        if not success:
            return Response({
                "query": "friendrequest",
                "success": False,
                "message": message
            }, status=400)
        if not friend_request:
            return Response({
                "query": "friendrequest",
                "success": False,
                "message": "Could not find a friend request from the specified author"
            }, status=404)

        # check if this is an external friendship
        localAuthorUrl = get_author_url(pk)
        if localAuthorUrl.split("/author/")[0] != friend_data["url"].split("/author/")[0]:
            xServerAuthorUrl = friend_data["url"]
            xServerBody = {
                "query": "friendrequest",
                "friend": friend_data,
                "author": {
                    "displayName": author.displayName,
                    "host": localAuthorUrl.split("/author/")[0],
                    "id": localAuthorUrl,
                    "url": localAuthorUrl
                }
            }
            print(xServerBody)
            server = ServerUtil(authorUrl=xServerAuthorUrl)
            # if we fail to notify the external server we can't proceed with the friendship
            if not server.is_valid() or not server.notify_server_of_friendship(xServerBody):
                return Response({
                    "query": "friendrequest",
                    "success": False,
                    "message": "Failed to notify external server."
                }, status=500)

        if (body["approve"]):
            Follow.objects.create(follower=get_author_url(pk), followed=friend_data["url"])
        friend_request.delete()
        response = {
            "message": message,
            "success": success,
            "query": "friendrequest"
        }
        return Response(response, status=200)

    ## Gets whether the author is following the one specified in the body
    @action(methods=['get'], detail=True, url_path='friends/(?P<other_user>.+)', url_name='friend_to_friend')
    def friend_to_friend_query(self, request, pk, other_user):
        try:
            author_url = Author.objects.get(pk=pk).get_url()
            other_url = other_user if "http" in other_user else get_author_url(other_user)

            follow = Follow.objects.filter(follower=author_url, followed=other_url)
            reverse = Follow.objects.filter(follower=other_url, followed=author_url)
        except:
            return Response({
                "success": False,
                "message": "Invalid author ID url parameter specified",
                "query": "friends"
            }, status=404)

        return Response({
            "query": "friends",
            "authors": [author_url, other_url],
            "friends": follow.exists() and reverse.exists()
        }, status=200)

    @action(methods=['get', 'post'], detail=True, url_path='friends', url_name='friends')
    def friends(self, request, pk):
        try:
            author = Author.objects.get(pk=pk)
        except:
            return Response({
                "query": "friends",
                "author": pk,
                "message": "The author ID was invalid",
                "success": False
            }, status=404)

        if (request.method == "POST"):
            return handle_friends_post(request, pk)

        return handle_friends_get(request, pk)

    @action(methods=['get'], detail=True, url_path='followed', url_name='followed_users')
    def list_followed_users(self, request, pk):
        author = get_object_or_404(Author, pk=pk)
        author_url = author.get_url()
        follows = Follow.objects.filter(follower=author_url)
        followed_urls = []
        for follow in follows:
            followed_urls.append(follow.followed)
        info = get_author_summaries(followed_urls)
        return Response({
            "query": "listFollowed",
            "followed": info
        }, status=200)

    @action(methods=['get'], detail=True, url_path='followers', url_name='follower_users')
    def list_follower_users(self, request, pk):
        author = get_object_or_404(Author, pk=pk)
        author_url = author.get_url()
        follows = Follow.objects.filter(followed=author_url)
        print("follows", len(follows))
        followed_urls = []
        for follow in follows:
            followed_urls.append(follow.follower)
        info = get_author_summaries(followed_urls)
        return Response({
            "query": "listFollowing",
            "followers": info
        }, status=200)

    @action(methods=['post'], detail=True, url_path='update', url_name='update')
    def update_profile(self, request, pk):
        try:
            author = Author.objects.get(pk=pk)
            if (request.user != author.user):
                return Response("Invalid authentication credentials" + str(request.user),
                                status=status.HTTP_403_FORBIDDEN)
        except:
            return Response("Invalid author ID specified", status=404)

        try:
            author.displayName = request.data["displayName"]
            author.user.first_name = request.data["firstName"]
            author.user.last_name = request.data["lastName"]
            if (request.data["email"]):
                email = request.data["email"].split("@")
                if (len(email) != 2):
                    raise ValueError
                author.user.email = request.data["email"]
            author.bio = request.data["bio"]
            if (request.data["github"] and (
                    "https://github.com/" not in request.data["github"] and "https://www.github.com/" not in
                    request.data["github"])):
                raise ValueError
            author.github = request.data["github"]
            author.user.full_clean()
            author.full_clean()
            author.user.save()
            author.save()
        except:
            return Response("The request body had missing or invalid values", status=400)

        return Response("The profile was successfully updated")

    ## Gets whether the author is following the one specified in the body
    @action(methods=['post'], detail=True, url_path='follows', url_name='is_following')
    def check_is_following(self, request, pk):
        try:
            Author.objects.get(pk=pk)
        except:
            return Response({
                "success": False,
                "message": "Invalid author ID url parameter specified"
            }, status=404)

        try:
            followed = request.data["author"]
            if ("/author/" not in followed):
                followed = get_author_url(followed)
            pk_url = get_author_url(pk)
            follow = Follow.objects.filter(follower=pk_url, followed=followed)
            reverse = Follow.objects.filter(follower=followed, followed=pk_url)
        except:
            return Response({
                "success": False,
                "message": "The author field was incorrect"
            }, status=400)

        return Response({
            "isFollowingUser": follow.exists(),
            "isOtherFollowing": reverse.exists(),
            "isOtherFriendRequest": FriendRequest.objects.filter(requester=followed, friend=pk_url).exists()
        }, status=200)

    # All posts the currently auth'd user can see of pk
    # /author/{AUTHOR_ID}/posts
    @action(detail=True, url_path="posts")
    def author_posts(self, request, pk=None):
        print("test, hit: author_posts with:", request, pk)
        page = int(request.query_params.get("page", 0)) + 1  # Must offset page by 1
        if page < 1:
            return Response({
                "query": "posts",
                "message": "Page number must be positive",
                "success": False
            }, status=400)

        size = int(request.query_params.get("size", DEFAULT_POST_PAGE_SIZE))
        if size < 0:
            return Response({
                "query": "posts",
                "message": "Size must be positive",
                "success": False
            }, status=400)
        elif size > 100:
            return Response({
                "query": "posts",
                "message": "The page size can not be greater than 100",
                "success": False
            }, status=400)

        try:
            if (is_encoded_external_host(pk)):
                return get_external_author_posts(request, pk)
            author = Author.objects.get(pk=pk)
        except:
            return Response({
                "query": "posts",
                "message": "You must specify an author.",
                "success": False
            }, status=400)

        # Only return public posts if the user isn't authenticated
        if request.user.is_anonymous:
            posts = Posts.objects.all().filter(author=pk, visibility__in=["PUBLIC"], unlisted=False)
        # else if is other_server:
        #     posts = Posts.objects.all().filter(author=pk, visibility__in=["PUBLIC"])
        elif (request.user.author == author):
            posts = Posts.objects.all().filter(author=pk, unlisted=False)
        else:
            requestingAuthor = request.user.author.id  # Should be guaranteed because we checked above

            # post_types will track what level of posts a user can see
            post_types = ["PUBLIC"]

            # convert to dict for dat O(1)
            # Note: this is terrible, we should be using the database more directly
            requesterFriends = {}
            for friend in get_friends_from_pk(requestingAuthor):
                friend = friend.split("/")[-1]
                requesterFriends[friend] = True

            # Check if they are direct friends
            if requesterFriends.get(str(pk), False):
                post_types += ["FRIENDS", "FOAF", "SERVERONLY"]
            else:  # They are not direct friends, so we should check if they share any friends
                for friend in get_friends_from_pk(pk):
                    friend = friend.split("/")[-1]
                    if requesterFriends.get(friend, False):
                        post_types += ["FOAF"]
                        break  # we don't need to check any more friends

            try:
                posts = Posts.objects.all().filter(author=pk, visibility__in=post_types, unlisted=False)
                # TODO: requestingAuthor is the one it should be visibleTo
                posts |= Posts.objects.all().filter(author=pk, visibility="PRIVATE",
                                                    visibleTo__contains=[get_author_url(str(requestingAuthor))],
                                                    unlisted=False)
            except:
                print("got except!")
                return Response(status=500)

        github_stream = get_github_activity(author)
        combined_stream = merge_posts_with_github_activity(posts, github_stream)

        pages = Paginator(combined_stream, size)
        current_page = pages.page(page)
        posts = PostsSerializer(current_page, many=True)
        response = {
            "query": "posts",
            "count": pages.count,
            "size": size,
            "posts": posts.data
        }
        add_page_details_to_response(request, response, current_page, page - 1)
        return Response(response, status=200)

    # All posts visible to the currently auth'd user
    # /author/posts
    @action(detail=False, url_path="posts")
    def visible_posts(self, request):
        print("visible_posts endpoint hit")
        xUser = request.META.get("HTTP_X_REQUEST_USER_ID")
        page = int(request.query_params.get("page", 0)) + 1  # Must offset page by 1
        if page < 1:
            return Response({
                "query": "posts",
                "message": "Page number must be positive",
                "success": False
            }, status=400)
        size = int(request.query_params.get("size", DEFAULT_POST_PAGE_SIZE))
        if size < 0 or size > 100:
            return Response({
                "query": "posts",
                "message": "Size was invalid",
                "success": False
            }, status=400)

        # Only return public posts if the user isn't authenticated
        if request.user.is_anonymous:
            posts = Posts.objects.all().filter(visibility__in=["PUBLIC"], unlisted=False)
        elif ServerUtil.is_server(request.user):
            sUtil = ServerUtil(user=request.user)
            if not sUtil.is_valid():
                return Response("This shouldn't happen, server=server!", status=500)
            elif not xUser:
                print("No xUser specified, sending all public posts")
                posts = Posts.objects.all().filter(visibility__in=["PUBLIC"])
            elif not sUtil.author_from_this_server(xUser):
                return Response(
                    "You're trying to access posts for a user that doesn't belong to you. user: " + xUser + " server: " + sUtil.get_base_url(),
                    status=400)
            else:
                followedByXUser = Follow.objects.values_list("followed", flat=True).filter(follower=xUser)
                friendsOfXUser = Follow.objects.values_list("follower", flat=True).filter(followed=xUser,
                                                                                          follower__in=followedByXUser)
                friends = []
                friends += sUtil.get_friends_of(xUser.split("/author/")[1])
                friends += friendsOfXUser
                friends = list(set(friends))
                foafs = []
                foafs += friends
                for friend in friends:
                    print("friend of", xUser, ":", friend)
                    # First check if it's an external user
                    sUtil = ServerUtil(authorUrl=friend)
                    if sUtil.is_valid():
                        foafs += sUtil.get_friends_of(friend.split("/author/")[1])
                    else:  # it's not external (local), or we don't have that node anymore
                        peopleFollowedByFriend = Follow.objects.values_list("followed", flat=True).filter(
                            follower=friend)
                        friendFriends = Follow.objects.values_list("follower", flat=True).filter(followed=friend,
                                                                                                 follower__in=peopleFollowedByFriend)
                        foafs += friendFriends
                baseUrl = get_host_url()
                foafs = list(set(foafs))
                friends = [get_author_id(x) for x in friends if x.startswith(baseUrl)]
                foafs = [get_author_id(x) for x in foafs if x.startswith(baseUrl)]
                posts = Posts.objects.all().filter(visibility="PUBLIC", unlisted=False)
                posts |= Posts.objects.all().filter(visibility="FRIENDS", author_id__in=friends, unlisted=False)
                posts |= Posts.objects.all().filter(visibility="FOAF", author_id__in=foafs, unlisted=False)
                posts |= Posts.objects.all().filter(visibility="PRIVATE", visibleTo__contains=[xUser], unlisted=False)
        else:
            requestingAuthor = request.user.author.id  # Should be guaranteed because not anon
            # Get direct friends and FOAFs into a dictionary
            requesterFriends = {}
            requesterFOAFs = {}
            for friend in get_friends_from_pk(requestingAuthor):
                # friend = friend.split("/")[-1] # these are actually "urls", so grab the uuid
                requesterFriends[friend] = True
            for friend in requesterFriends:
                for foaf in get_friends(friend):
                    # friend = friend.split("/")[-1] # these are actually "urls", so grab the uuid
                    # Ensure we don't add direct friends as an FOAF
                    if not requesterFriends.get(foaf, False):
                        requesterFOAFs[foaf] = True
            try:
                # Grab the requesting user's posts
                posts = Posts.objects.all().filter(author=requestingAuthor, unlisted=False)
                # Grab all public posts
                posts |= Posts.objects.all().filter(visibility__in=["PUBLIC"], unlisted=False)

                host_url = get_host_url()
                # Grab posts from direct friends
                for friend in requesterFriends:
                    if not friend.startswith(host_url): continue
                    posts |= Posts.objects.all().filter(author=get_author_id(friend),
                                                        visibility__in=["FRIENDS", "FOAF", "SERVERONLY"],
                                                        unlisted=False)

                # Posts from FOAFs
                for friend in requesterFOAFs:
                    if not friend.startswith(host_url): continue
                    posts |= Posts.objects.all().filter(author=get_author_id(friend), visibility__in=["FOAF"],
                                                        unlisted=False)

                # PRIVATE posts that the author can see
                posts |= Posts.objects.all().filter(visibility="PRIVATE",
                                                    visibleTo__contains=[get_author_url(str(requestingAuthor))],
                                                    unlisted=False)
            except:
                print("got except!")
                return Response(status=500)

        pages = Paginator(posts, size)
        current_page = pages.page(page)
        posts = PostsSerializer(current_page, many=True)

        response = {
            "query": "posts",
            "count": pages.count,
            "size": size,
            "posts": posts.data
        }
        add_page_details_to_response(request, response, current_page, page - 1)
        return Response(response, status=200)
