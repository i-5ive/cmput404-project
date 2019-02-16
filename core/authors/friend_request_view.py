import json

from rest_framework.decorators import api_view
from rest_framework.response import Response

from core.authors.models import Author, Follow, FriendRequest
from core.authors.serializers import AuthorSummarySerializer

from core.authors.util import get_author_id
from core.hostUtil import is_external_host

def are_authors_friends(author_one, author_two):
    return Follow.objects.filter(follower=author_one, friend=author_two).exists() and Follow.objects.filter(follower=author_two, friend=author_one).exists()
    
def get_author_details(raw_object):
    data = AuthorSummarySerializer(data=raw_object)
    data.is_valid(raise_exception=True)
    return data.validated_data

def parse_request_body(request):
    body = request.data
        
    if body["query"] != "friendrequest":
        return Response({
            "query": "friendrequest",
            "success": False,
            "message": "The query value was not correct"
        }, status=400)
    
    author = get_author_details(body["author"])
    friend = get_author_details(body["friend"])
    
    authorId = get_author_id(author["id"])
    friendId = get_author_id(friend["id"])
    
    externalAuthor = is_external_host(author["host"])
    externalFriend = is_external_host(friend["host"])

    return (author, friend, authorId, friendId, externalAuthor, externalFriend)

def validate_friend_details(authorId, friendId, externalAuthor, externalFriend, authorUrl, friendUrl):
    success = True
    message = "Friend request sent"

    if (externalAuthor and externalFriend):
        success = False
        message = "Neither user belongs to this server"
    elif (authorId == friendId):
        success = False
        message = "The requesting user was the same as the followed user"
    elif (FriendRequest.objects.filter(requester=authorUrl, friend=friendUrl).exists() or FriendRequest.objects.filter(friend=authorUrl, requester=friendUrl).exists()):
        success = False
        message = "The two authors already have a friend request pending"
    elif (not externalAuthor and not Author.objects.filter(id=authorId).exists()) or (not externalFriend and not Author.objects.filter(id=friendId).exists()):
        success = False
        message = "At least one of the two authors are not external and do not exist on this server"
    elif (Follow.objects.filter(follower=authorUrl, followed=friendUrl).exists()):
        success = False
        message = "The requester is already following this friend"
    return (success, message)

@api_view(['POST'])
def handle_follow_request(request):
    try:
        author, friend, authorId, friendId, externalAuthor, externalFriend = parse_request_body(request)
        authorUrl = author["url"]
        friendUrl = friend["url"]
    except Exception as e:
        return Response({
                "query": "friendrequest",
                "success": False,
                "message": "The body did not contain all of the required parameters"
            }, status=400)
    
    success, message = validate_friend_details(authorId, friendId, externalAuthor, externalFriend, authorUrl, friendUrl)

    if not success:
        return Response({
            "query": "friendrequest",
            "success": False,
            "message": message
        }, status=400)

    # TODO: update other server if remote host
    
    reverseFollow = Follow.objects.filter(follower=friendUrl, followed=authorUrl)
    if not reverseFollow.exists():
        request = FriendRequest.objects.create(requester=authorUrl, friend=friendUrl, requester_name=author["displayName"])
        request.save()

    follow = Follow.objects.create(follower=authorUrl, followed=friendUrl)
    follow.save()

    return Response({
        "query": "friendrequest",
        "success": True,
        "message": message
    }, status=200)