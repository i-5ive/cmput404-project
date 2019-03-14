from rest_framework.decorators import api_view
from rest_framework.response import Response

from core.authors.models import Author
from django.contrib.auth import authenticate

QUERY = "login"
LOGIN_TIME_IN_SECONDS = 86400 # 24 hours

def handle_request(request):
    success = True
    message = "You have been signed in successfully"

    username = request.data["username"]
    password = request.data["password"]
    userId = None

    if (request.data["query"] != QUERY):
        success = False
        message = "The query value was not correct"
    else:
        user = authenticate(username=username, password=password)
        if user:
            author = Author.objects.get(user=user)
            if (author.approved):
                userId = author.id
            else:
                success = False
                message = "This account has not been approved by an administrator yet"
        else:
            success = False
            message = "The provided credentials were incorrect"
            
    return (success, message, userId)

@api_view(['POST'])
def login(request):
    try:
        success, message, userId = handle_request(request)
    except:
        return Response({
                "query": QUERY,
                "success": False,
                "message": "The body did not contain all of the required parameters"
            }, status=400)
  
    response = Response({
        "query": QUERY,
        "success": success,
        "message": message
    })
    if success:
        response.set_cookie("core-username", request.data["username"], max_age=LOGIN_TIME_IN_SECONDS)
        response.set_cookie("core-userid", str(userId), max_age=LOGIN_TIME_IN_SECONDS)
        response.set_cookie("core-password", request.data["password"], max_age=LOGIN_TIME_IN_SECONDS)
        response.status_code = 200
    else:
        response.status_code = 400

    return response