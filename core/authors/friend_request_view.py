from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from core.authors.models import Author, Follow, FriendRequest
from core.authors.serializers import AuthorSummarySerializer

from core.authors.util import get_author_id, get_author_url
from core.hostUtil import is_external_host

from core.servers.SafeServerUtil import ServerUtil

def are_authors_friends(author_one, author_two):
    return Follow.objects.filter(follower=author_one, friend=author_two).exists() and Follow.objects.filter(follower=author_two, friend=author_one).exists()
    
def get_author_details(raw_object):
    data = AuthorSummarySerializer(data=raw_object)
    data.is_valid(raise_exception=True)
    return raw_object

def validate_request_body(request):
    body = request.data
        
    if body["query"] != "friendrequest":
        raise ValueError
    
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
        message = "One of the authors must be from this server, neither could be found on this server"
    elif (Follow.objects.filter(follower=authorUrl, followed=friendUrl).exists()):
        success = False
        message = "The requester is already following this friend"
    return (success, message)

@api_view(['POST'])
def handle_follow_request(request):
    user = request.user
    # Block unauthenticated requests
    if not user.is_authenticated:
        return Response({
            "query": "friendrequest",
            "success": False,
            "message": "You must be authenticated to perform that action."
        }, status=status.HTTP_403_FORBIDDEN)

    print("handle_follow_request received", request.body)

    # validate_request_body(...) will helplessly throw if there are errors in the request
    # wrangle those errors and deny the request in that case
    try:
        author, friend, authorId, friendId, externalAuthor, externalFriend = validate_request_body(request)
    except Exception as e:
        print(e)
        return Response({
            "query": "friendrequest",
            "success": False,
            "message": "The body did not contain all of the required parameters"
        }, status=400)

    # If it's an author making the request, ensure it's the correct user sending the request
    # In most cases this wouldn't happen, unless there's malformed data or hackerz editing the json
    if not ServerUtil.is_server(user) and get_author_url(str(request.user.author.pk)) != author["url"]:
        # TODO: remove the debug message later
        return Response({
            "query": "friendrequest",
            "success": False,
            "message": "You must be authenticated as the requester to perform this action.",
            "debug": get_author_url(str(request.user.author.pk if request.user.is_authenticated else "/author/awoejaiweowae")) + " should be " + author["url"]
        }, status=status.HTTP_403_FORBIDDEN)
    elif ServerUtil.is_server(user):
        pass
    else:
        assert(False, "This should never happen...")
    
    # Extract the URLs into variables
    authorUrl = author["url"]
    friendUrl = friend["url"]
    success, message = validate_friend_details(authorId, friendId, externalAuthor, externalFriend, authorUrl, friendUrl)
    if not success:
        return Response({
            "query": "friendrequest",
            "success": False,
            "message": message
        }, status=400)

    # Local Author follows foreign author, need to tell foreign server what's up
    if externalFriend:
        server = ServerUtil(authorUrl=friendUrl)
        if not server.is_valid() or not server.notify_server_of_friendship(request.data):
            return Response({
                "query": "friendrequest",
                "success": False,
                "message": "Failed to notify external server."
            }, status=500)
    # We only want to track friend requests locally because creating a friend request
    # for an external server will block it from using the official APIs because "a friend
    # request already exists".
    else:
        reverseFollow = Follow.objects.filter(follower=friendUrl, followed=authorUrl)
        if not reverseFollow.exists():
            FriendRequest.objects.create(requester=authorUrl, friend=friendUrl)

    Follow.objects.create(follower=authorUrl, followed=friendUrl)

    return Response({
        "query": "friendrequest",
        "success": True,
        "message": message
    }, status=200)