import base64
import json

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from core.posts.models import Posts
from core.authors.models import Author
from core.posts.serializers import PostsSerializer
from core.users.models import User

from core.authors.util import get_author_id

MAX_UPLOAD_SIZE = 10485760
    
def create_post(request, data):
    success = True
    message = "Post created"

    post_serializer = PostsSerializer(data=data)
    post_serializer.is_valid()
    new_post = post_serializer.save()

    # if image, make another post with generated post_id
    if (request.FILES):
        # Credits to Justin Voss, https://stackoverflow.com/a/856126
        for img_file in request.FILES.getlist('imageFiles'):
            new_id = new_post.post_id
            image_type = img_file.content_type
            image_size = img_file.size
            
            if image_type == "image/jpeg" or image_type == "image/png":
                content_type = "%s;base64" % image_type
            elif (image_type == "application/base64"):
                content_type = image_type
            else:
                return False, "Invalid file type", None

            # http://www.learningaboutelectronics.com/Articles/How-to-restrict-the-size-of-file-uploads-with-Python-in-Django.php
            if image_size > MAX_UPLOAD_SIZE:
                return False, "The maximum file size that can be uploaded is 10MB", None

            # Credits to Ykh, https://stackoverflow.com/a/44492948
            # Credits to Willem Van Onsem, https://stackoverflow.com/a/52444999
            encoded_image = content_type + "," + base64.b64encode(img_file.read()).decode()

            data["post_id"] = new_id
            data["content"] = str(encoded_image)
            data["contentType"] = content_type
            data["unlisted"] = True

            serializer = PostsSerializer(data=data)
            serializer.is_valid()
            serializer.save()

    return success, message, post_serializer.data

def handle_visible_to(request, data):
    visible_to = request.data.get("visibleTo")
    if (visible_to):
        visible_to = json.loads(visible_to)
        externalUsers = [x for x in visible_to if x.startswith("https://")]
        users = User.objects.filter(username__in=visible_to)
        if (len(users)+len(externalUsers) == len(visible_to)):
            data["visibleTo"] = []
            found_self = False
            for user in users:
                data["visibleTo"].append(user.author.get_url())
                if (user == request.user):
                    found_self = True
            if (not found_self):
                data["visibleTo"].append(request.user.author.get_url())
            data["visibleTo"] += externalUsers
        else:
            invalid_users = []
            seen_users = {}
            for user in users:
                seen_users[user] = True
            for user in visible_to:
                if (not seen_users.get(user)):
                    invalid_users.append(user)
            return Response({
                "success": False,
                "query": request.data["query"],
                "message": "Not all requested users could be found",
                "invalidUsers": invalid_users
            }, status=400)

def handle_posts(request):
    query = request.data["query"]
    data = json.loads(request.data["postData"])
    if ((not request.user.is_authenticated) or str(request.user.author.id) != data["author"]):
        return Response({
            "success": False,
            "query": query,
            "message": "You are not authenticated as the post's specified author",
            "post": None
        }, status=status.HTTP_403_FORBIDDEN)
    success = False
    message = "There was a problem parsing the request body"

    visible_to_response = handle_visible_to(request, data)
    if (visible_to_response):
        return visible_to_response
    
    try:
        success, message, new_post = create_post(request, data)
    except:
        new_post = None
    
    if success: 
        code = 200
    else:
        code = 400

    return Response({
        "success": success,
        "query": query,
        "message": message,
        "post": new_post
    }, status=code)