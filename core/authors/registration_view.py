from rest_framework.decorators import api_view
from rest_framework.response import Response

from core.authors.models import Author
from core.users.models import User

from core.authors.util import get_author_id

REGISTER = "register"

def validate_request_body(query, username, password):
    success = True
    message = "Your account has been created and is pending approval"
    if (query != REGISTER):
        success = False
        message = "The query value was not correct"
    elif (len(username) == 0):
        success = False
        message = "Usernames can not be empty"
    elif (len(password) < 6):
        success = False
        message = "Passwords must be at least 6 characters long"
    elif (len(password) > 24):
        success = False
        message = "Passwords can not be more than 24 characters long"
    elif (len(username) > 24):
        success = False
        message = "Usernames can not be more than 24 characters long"
    elif (User.objects.filter(username=username).exists()):
        success = False
        message = "This username is already being used by someone"
    return (success, message)

@api_view(['POST'])
def register_new_user(request):
    try:
        username = request.data["username"]
        password = request.data["password"]
        success, message = validate_request_body(request.data["query"], username, password)
    except:
        return Response({
                "query": REGISTER,
                "success": False,
                "message": "The body did not contain all of the required parameters"
            }, status=400)
    
    if not success:
        return Response({
            "query": REGISTER,
            "success": False,
            "message": message
        }, status=400)

    User.objects.create(username=username, password=password)
    return Response({
        "query": REGISTER,
        "success": True,
        "message": message
    }, status=200)