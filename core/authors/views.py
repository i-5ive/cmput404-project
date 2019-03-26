from django.core.paginator import Paginator

from rest_framework import viewsets, status
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404

from core.authors.models import Author, Follow, FriendRequest
from core.authors.serializers import AuthorSerializer, AuthorSummarySerializer
from core.authors.friend_request_view import get_author_details

from core.authors.util import get_author_url, get_author_summaries, get_author_id
from core.authors.friends_view import handle_friends_get, handle_friends_post
from core.hostUtil import get_host_url
from core.authors.friends_util import get_friends, get_friends_from_pk

from core.posts.models import Posts
from core.posts.serializers import PostsSerializer
from core.posts.constants import DEFAULT_POST_PAGE_SIZE

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
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

    def retrieve(self, request, pk):
        try:
            author = Author.objects.get(pk=pk)
        except:
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

    @action(methods=['post'], detail=True, url_path='friendrequests/respond', url_name='friend_requests_respond')
    def handle_friend_request_response(self, request, pk):
        try:
            author = Author.objects.get(pk=pk)
            if ((not request.user.is_authenticated) or request.user.author != author):
                return Response({
                    "query": "friendResponse",
                    "success": False,
                    "message": "You must be authenticated as the requested user to perform this action."
                }, status=status.HTTP_403_FORBIDDEN)
        except:
            return Response({
                "query": "friendResponse",
                "success": False,
                "message": "Invalid author ID specified"
            }, status=404)
        
        try:
            message = "The request body could not be parsed"
            body = request.data
            success, message, friend_request, friend_data = validate_friend_request_response(body, pk)
        except:
            return Response({
                "query": "friendResponse",
                "success": False,
                "message": message
            }, status=400)
        
        if not success:
            return Response({
                "query": "friendResponse",
                "success": False,
                "message": message
            }, status=400)
        if not friend_request:
            return Response({
                "query": "friendResponse",
                "success": False,
                "message": "Could not find a friend request from the specified author"
            }, status=404)

        if (body["approve"]):
            Follow.objects.create(follower=get_author_url(pk), followed=friend_data["url"])

        friend_request.delete()
        response = {
            "message": "Your response has been recorded",
            "success": success,
            "query": message
        }
        return Response(response, status=200)

    ## Gets whether the author is following the one specified in the body
    @action(methods=['get'], detail=True, url_path='friends/(?P<other_user>[^/.]+)', url_name='friend_to_friend')
    def friend_to_friend_query(self, request, pk, other_user):
        try:
            author_url = Author.objects.get(pk=pk).get_url()
            other_url = get_author_url(other_user)
            
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
                return Response("Invalid authentication credentials" + str(request.user), status=status.HTTP_403_FORBIDDEN)
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
            if (request.data["github"] and ("https://github.com/" not in request.data["github"] and "https://www.github.com/" not in request.data["github"])):
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
        page = int(request.query_params.get("page", 0)) + 1 # Must offset page by 1
        if page < 1:
            return Response({
                "query": "posts",
                "message": "Page number must be positive",
                "success": False
            }, status=400)

        # TODO: size should be limited?
        size = int(request.query_params.get("size", DEFAULT_POST_PAGE_SIZE))
        if size < 0:
            return Response({
                "query": "posts",
                "message": "Size must be positive",
                "success": False
            }, status=400)

        if not pk:
            return Response({
                "query": "posts",
                "message": "You must specify an author.",
                "success": False
            }, status=400)

        # Only return public posts if the user isn't authenticated
        if request.user.is_anonymous:
            posts = Posts.objects.all().filter(author=pk, visibility__in=["PUBLIC", "SERVERONLY"], unlisted=False)
        # else if is other_server:
        #     posts = Posts.objects.all().filter(author=pk, visibility__in=["PUBLIC"])
        else:
            requestingAuthor = request.user.author.id # Should be guaranteed because we checked above

            # post_types will track what level of posts a user can see
            post_types = ["PUBLIC", "SERVERONLY"]
            # convert to dict for dat O(1)
            # Note: this is terrible, we should be using the database more directly
            requesterFriends = {}
            for friend in get_friends_from_pk(requestingAuthor):
                friend = friend.split("/")[-1]
                requesterFriends[friend] = True

            # Check if they are direct friends
            if requesterFriends.get(str(pk), False):
                post_types += ["FRIENDS", "FOAF"]
            else: # They are not direct friends, so we should check if they share any friends
                for friend in get_friends_from_pk(pk):
                    friend = friend.split("/")[-1]
                    if requesterFriends.get(friend, False):
                        post_types += ["FOAF"]
                        break # we don't need to check any more friends

            try:
                posts = Posts.objects.all().filter(author=pk, visibility__in=post_types, unlisted=False)
                # TODO: requestingAuthor is the one it should be visibleTo
                posts |= Posts.objects.all().filter(author=pk, visibility="PRIVATE", visibleTo__contains=[get_author_url(str(requestingAuthor))], unlisted=False)
            except:
                print("got except!")
                return Response(status=500)

        pages = Paginator(posts, size)
        posts = PostsSerializer(pages.page(page), many=True)

        response = {
            "query": "posts",
            "count": pages.count,
            "size": size,
            # Recall: the page the user specifies is offset by +1 for Paginator
            "next": "/author/{}/posts?page={}".format(pk,page) if page < pages.num_pages else None,
            "previous": "/author/{}/posts?page={}".format(pk,page-2) if page > 1 else None,
            "posts": posts.data
        }
        return Response(response, status=200)

    # All posts visible to the currently auth'd user
    # /author/posts
    @action(detail=False, url_path="posts")
    def visible_posts(self, request):
        page = int(request.query_params.get("page", 0)) + 1 # Must offset page by 1
        if page < 1:
            return Response({
                "query": "posts",
                "message": "Page number must be positive",
                "success": False
            }, status=400)
        # TODO: size should be limited?
        size = int(request.query_params.get("size", DEFAULT_POST_PAGE_SIZE))
        if size < 0:
            return Response({
                "query": "posts",
                "message": "Size must be positive",
                "success": False
            }, status=400)

        # Only return public posts if the user isn't authenticated
        if request.user.is_anonymous:
            posts = Posts.objects.all().filter(visibility__in=["PUBLIC", "SERVERONLY"], unlisted=False)
        elif ServerUtil.is_server(request.user):
            posts = Posts.objects.all().filter(visibility__in=["PUBLIC"])
            # do extra based on header?
        else:
            requestingAuthor = request.user.author.id # Should be guaranteed because not anon
            # Get direct friends and FOAFs into a dictionary
            requesterFriends = {}
            requesterFOAFs = {}
            for friend in get_friends_from_pk(requestingAuthor):
                friend = friend.split("/")[-1] # these are actually "urls", so grab the uuid
                requesterFriends[friend] = True
            for friend in requesterFriends:
                for friend in get_friends_from_pk(friend):
                    friend = friend.split("/")[-1] # these are actually "urls", so grab the uuid
                    # Ensure we don't add direct friends as an FOAF
                    if not requesterFriends.get(friend, False):
                        requesterFOAFs[friend] = True
            try:
                # Grab the requesting user's posts
                posts = Posts.objects.all().filter(author=requestingAuthor, unlisted=False)
                # Grab all public posts
                posts |= Posts.objects.all().filter(visibility__in=["PUBLIC", "SERVERONLY"], unlisted=False)

                # Grab posts from direct friends
                for friend in requesterFriends:
                    posts |= Posts.objects.all().filter(author=friend, visibility__in=["FRIENDS", "FOAF"], unlisted=False)

                # Posts from FOAFs
                for friend in requesterFOAFs:
                    posts |= Posts.objects.all().filter(author=friend, visibility__in=["FOAF"], unlisted=False)

                # PRIVATE posts that the author can see
                posts |= Posts.objects.all().filter(visibility="PRIVATE", visibleTo__contains=[get_author_url(str(requestingAuthor))], unlisted=False)
            except:
                print("got except!")
                return Response(status=500)
        
        pages = Paginator(posts, size)
        posts = PostsSerializer(pages.page(page), many=True)

        response = {
            "query": "posts",
            "count": pages.count,
            "size": size,
            # Recall: the page the user specifies is offset by +1 for Paginator
            "next": "/author/posts?page={}".format(page) if page < pages.num_pages else None,
            "previous": "/author/posts?page={}".format(page-2) if page > 1 else None,
            "posts": posts.data
        }
        return Response(response, status=200)