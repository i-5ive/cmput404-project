from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from core.authors.models import Author, Follow, FriendRequest
from core.authors.serializers import AuthorSummarySerializer

QUERY = "unfollow"

def validate_author_details(raw_object):
    data = AuthorSummarySerializer(data=raw_object)
    data.is_valid(raise_exception=True)

def validate_request_body(request):
    body = request.data
        
    if body["query"] != QUERY:
        raise ValueError
    
    validate_author_details(body["author"])
    validate_author_details(body["requester"])

@api_view(['POST'])
def handle_unfollow_request(request):
    try:
        validate_request_body(request)
        authorUrl = request.data["author"]["url"]
        requesterUrl = request.data["requester"]["url"]
        
        if ((not request.user.is_authenticated) or request.user.author.get_url() != requesterUrl):
            return Response({
                "query": QUERY,
                "success": False,
                "message": "You are not authenticated as the requesting user"
            }, status=status.HTTP_403_FORBIDDEN)

        follow = Follow.objects.get(follower=requesterUrl, followed=authorUrl)
        friendRequest = FriendRequest.objects.filter(requester=requesterUrl, friend=authorUrl)
    except:
        return Response({
                "query": QUERY,
                "success": False,
                "message": "The body did not contain all of the required parameters"
            }, status=400)
    
    follow.delete()
    if (friendRequest.exists()):
        friendRequest.delete()

    return Response({
        "query": QUERY,
        "success": True,
        "message": "The author was unfollowed successfully"
    }, status=200)