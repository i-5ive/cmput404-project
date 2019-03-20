from rest_framework.response import Response

from core.authors.friends_util import get_friends, get_friends_set
from core.authors.util import get_author_url

def parse_is_friends_with_any(data, authorUrl):
    success = True
    message = None

    if (data["query"] != "friends"):
        success = False
        message = "The query value was not correct"
    elif (data["author"] != authorUrl):
        success = False
        message = "The author in the body was not the same as the one in the URI"
    elif (type(data["authors"]) is not list):
        success = False
        message = "The authors value was not a list"
    
    return (success, message)

def handle_friends_get(request, pk):
    authorUrl = get_author_url(pk)

    return Response({
        "query": "friends",
        "authors": get_friends(authorUrl)
    }, status=200)

def handle_friends_post(request, pk):
    try:
        authorUrl = get_author_url(pk)
        success, message = parse_is_friends_with_any(request.data, authorUrl)
    except:
        return Response({
            "query": "friends",
            "author": authorUrl,
            "message": "There was an error parsing the request body",
            "success": False
        }, status=400)

    if not success:
        return Response({
            "query": "friends",
            "author": authorUrl,
            "message": message,
            "success": False
        }, status=400)

    authors = set(request.data["authors"])

    return Response({
        "query": "friends",
        "author": authorUrl,
        "authors": list(authors.intersection(get_friends_set(authorUrl)))
    }, status=200)
