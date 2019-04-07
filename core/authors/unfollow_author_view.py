from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from core.authors.models import Author, Follow, FriendRequest
from core.authors.serializers import AuthorSummarySerializer

from core.servers.SafeServerUtil import ServerUtil

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

# local: author, requester
# remote: author, friend
@api_view(['POST'])
def handle_unfollow_request(request):
    user = request.user
    try:
        if request.data.get("query", None) != "unfollow":
            raise Exception("You should specify that this is a 'unfollow' query.")
        authorData = request.data["author"]
        # Get friend, or requestor from the request body (both are allowed)
        requesterData = request.data.get("requester", request.data.get("friend", False))
        if not requesterData or not authorData:
            raise Exception("You need to specify an author and a 'requester' or 'friend'")
        authorUrl = authorData.get("id", authorData.get("url", False))
        requesterUrl = requesterData.get("id", requesterData.get("url", False))
        if not authorUrl or not requesterUrl:
            raise Exception("You must specify a 'url' or 'id' of each author and friend/requestor")

        if ServerUtil.is_server(user): # A foreign server is trying to unfriend one of our authors
            # because we share "author" key but foreign servers use this to be the "requestor" 
            # ("friend" is who to unfriend
            authorUrl, requesterUrl = requesterUrl, authorUrl
            print(authorUrl, requesterUrl)
            requesterServer = ServerUtil(authorUrl=requesterUrl)
            if not requesterServer.is_valid():
                return Response("Could not find a foreign node with the author's base url: "+authorUrl, status=400)
            serverServer = ServerUtil(user=user)
            if not serverServer.is_valid():
                return Response("This shouldn't happen... (server user is not valid).", status=400)
            if not serverServer.get_base_url() == requesterServer.get_base_url():
                return Response("You cannot change another server's author's following status.", status=400)

            try:
                follow = Follow.objects.get(follower=requesterUrl, followed=authorUrl)
                friendRequest = FriendRequest.objects.filter(requester=requesterUrl, friend=authorUrl)
            except:
                return Response("It seems these users are already not following each other.", status=400)
        else: # A local author is most likely unfollowing someone
            if ((not request.user.is_authenticated) or request.user.author.get_url() != requesterUrl):
                return Response({
                    "query": QUERY,
                    "success": False,
                    "message": "You are not authenticated as the requesting user"
                }, status=status.HTTP_403_FORBIDDEN)
            follow = Follow.objects.get(follower=requesterUrl, followed=authorUrl)
            friendRequest = FriendRequest.objects.filter(requester=requesterUrl, friend=authorUrl)
            # TODO: Should probably check if it is a foreign server first...
            sUtil = ServerUtil(authorUrl=authorUrl)
            if sUtil.is_valid(): # This server is remote and attached, notify them of the unfollow
                sUtil.notify_of_unfriendship(requesterUrl, authorUrl)
    except Exception as e:
        print("There was an error unfollowing: " + str(e)) # don't remove this or I'll cut you :)
        return Response({
            "query": QUERY,
            "success": False,
            "message": "Failed to unfollow, error: " + str(e)
        }, status=400)
    
    follow.delete()
    if (friendRequest.exists()):
        friendRequest.delete()

    return Response({
        "query": QUERY,
        "success": True,
        "message": "The author was unfollowed successfully"
    }, status=200)