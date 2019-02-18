from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework.decorators import api_view, action
from rest_framework.response import Response

from core.authors.models import Author, Follow, FriendRequest
from core.authors.serializers import AuthorSerializer, AuthorSummarySerializer
from core.authors.friend_request_view import get_author_details

from core.authors.util import get_author_url
from core.authors.friends_view import handle_friends_get, handle_friends_post

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

    @action(methods=['get'], detail=True, url_path='friendrequests', url_name='friend_requests')
    def get_friend_requests(self, request, pk):
        if (not Author.objects.filter(pk=pk).exists()):
            return Response("Invalid author ID specified", status=404)
        
        requests = FriendRequest.objects.filter(friend=get_author_url(pk))
        formatted_requests = []
        for pending_request in requests:
            formatted_requests.append({
                'displayName': pending_request.requester_name,
                'id': pending_request.requester,
                'host': pending_request.requester.split("/author/")[0],
                'url': pending_request.requester
            })
        return Response(formatted_requests, status=200)

    @action(methods=['post'], detail=True, url_path='friendrequests/respond', url_name='friend_requests_respond')
    def handle_friend_request_response(self, request, pk):
        if (not Author.objects.filter(pk=pk).exists()):
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
        if (not Author.objects.filter(pk=pk).exists()):
            return Response("Invalid author ID specified", status=404)
        
        if (request.method == "POST"):
            return handle_friends_post(request, pk)

        return handle_friends_get(request, pk)
