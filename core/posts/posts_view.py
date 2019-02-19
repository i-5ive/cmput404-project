import base64
import json

from rest_framework.decorators import api_view
from rest_framework.response import Response

from core.posts.models import Posts
from core.authors.models import Author
from core.posts.serializers import PostsSerializer

from core.authors.util import get_author_id

def delete_post(request):
    pass

def create_post(request):
    success = True
    message = "Post created"

    body = request.data
    data = json.loads(body["post_data"])

    serializer = PostsSerializer(data=data)
    serializer.is_valid()
    new_post = serializer.save()

    # if image, make another post with generated post_id
    # TODO Multi Image Posts?
    if (request.FILES):
        new_id = new_post.post_id
        image_type = request.FILES["imageFiles"].content_type
        
        if image_type == "image/jpeg" or image_type == "image/png":
            content_type = f"{image_type};base64"
        else:
            success = False
            message = "Invalid file type"
            return success, message

        # https://stackoverflow.com/questions/44489375/django-have-admin-take-image-file-but-store-it-as-a-base64-string
        encoded_image = base64.encodestring(request.FILES["imageFiles"].read())

        data["post_id"] = new_id
        data["content"] = str(encoded_image)
        data["contentType"] = content_type

        serializer = PostsSerializer(data=data)
        serializer.is_valid()
        serializer.save()

    return success, message


@api_view(['POST'])
def handle_posts(request):
    success = False
    message = "Invalid Query"

    query = request.data["query"]
        
    if query == "createpost":
        success, message = create_post(request)

    #TODO Delete Post

    if success: 
        code = 200
    else:
        code = 400

    return Response({
        "query": query,
        "success": success,
        "message": message
    }, status=code)