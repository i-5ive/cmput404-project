from rest_framework import viewsets
from rest_framework.decorators import api_view, action
from rest_framework.response import Response

from core.authors.models import Author, Follow, FriendRequest
from core.authors.serializers import AuthorSerializer, AuthorSummarySerializer
from core.authors.friend_request_view import get_author_details

from core.authors.util import get_author_url, get_author_summaries
from core.authors.friends_view import handle_friends_get, handle_friends_post
from core.hostUtil import get_host_url
from core.authors.friends_util import get_friends

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
        urls = []
        for pending_request in requests:
            urls.append(pending_request.requester)
        formatted_requests = get_author_summaries(urls)
        return Response(formatted_requests, status=200)

    @action(methods=['post'], detail=True, url_path='friendrequests/respond', url_name='friend_requests_respond')
    def handle_friend_request_response(self, request, pk):
        try:
            author = Author.objects.get(pk=pk)
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

    @action(methods=['get', 'post'], detail=True, url_path='friends', url_name='friends')
    def friends(self, request, pk):
        try:
            author = Author.objects.get(pk=pk)
        except:
            return Response("Invalid author ID specified", status=404)
        
        if (request.method == "POST"):
            return handle_friends_post(request, pk)

        return handle_friends_get(request, pk)

    @action(methods=['post'], detail=True, url_path='update', url_name='update')
    def update_profile(self, request, pk):
        try:
            author = Author.objects.get(pk=pk)
            if (request.user != author.user):
                return Response("Invalid authentication credentials" + str(request.user), status=401)
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
            follow = Follow.objects.filter(follower=get_author_url(pk), followed=followed)
        except:
            return Response({
                "success": False,
                "message": "The author field was incorrect"
            }, status=400)
        
        return Response({
            "isFollowingUser": follow.exists()
        }, status=200)