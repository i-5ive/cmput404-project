import json

from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from core.authors.models import Author, Follow, FriendRequest
from core.authors.serializers import AuthorSerializer, FriendAuthorSerializer

from core.authors.util import get_author_id
from core.hostUtil import is_external_host

class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

def are_authors_friends(author_one, author_two):
	return Follow.objects.filter(follower=author_one, friend=author_two, default=True).exists()
	
def get_author_details(raw_object):
	data = FriendAuthorSerializer(data=raw_object)
	data.is_valid(raise_exception=True)
	return data.validated_data

@api_view(['POST'])
def handle_follow_request(request):
	body = json.loads(request.body.decode("utf8"))
	
	if body["query"] != "friendrequest":
		return Response(status=400)
	
	author = get_author_details(body["author"])
	friend = get_author_details(body["friend"])
	
	authorId = get_author_id(author["id"])
	friendId = get_author_id(friend["id"])
	
	externalAuthor = is_external_host(author["host"])
	externalFriend = is_external_host(friend["host"])
	
	# TODO: update other server if remote host
	# TODO: update database locally
	
	if FriendRequest.objects.filter(requester=authorId, friend=friendId).exists() or FriendRequest.objects.filter(friend=authorId, requester=friendId).exists() or
		are_authors_friends(authorId, friendId) or (externalAuthor and externalFriend):
		return Response(status=400)
	elif (not externalAuthor and not Author.objects.filter(id=authorId).exists()) or (not externalFriend and not Author.objects.filter(id=friendId).exists()):
		return Response(status=400)
	
    return Response(status=200)