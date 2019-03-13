import base64
import json

from rest_framework.decorators import api_view
from rest_framework.response import Response

from core.posts.models import Posts
from core.authors.models import Author
from core.posts.serializers import PostsSerializer

from core.authors.util import get_author_id

MAX_UPLOAD_SIZE = 10485760
    
def create_post(request):
    success = True
    message = "Post created"

    body = request.data
    data = json.loads(body["postData"])

    post_serializer = PostsSerializer(data=data)
    post_serializer.is_valid()
    # TODO Remove this, leave in for now
    print(post_serializer.errors)
    new_post = post_serializer.save()

    # if image, make another post with generated post_id
    if (request.FILES):
        # Credits to Justin Voss, https://stackoverflow.com/questions/851336/multiple-files-upload-using-same-input-name-in-django
        for img_file in request.FILES.getlist('imageFiles'):
            new_id = new_post.post_id
            image_type = img_file.content_type
            image_size = img_file.size
            
            if image_type == "image/jpeg" or image_type == "image/png":
                content_type = "%s;base64" % image_type
            else:
                return False, "Invalid file type", None

            # http://www.learningaboutelectronics.com/Articles/How-to-restrict-the-size-of-file-uploads-with-Python-in-Django.php
            if image_size > MAX_UPLOAD_SIZE:
                return False, "The maximum file size that can be uploaded is 10MB", None

            # Credits to Ykh, https://stackoverflow.com/questions/44489375/django-have-admin-take-image-file-but-store-it-as-a-base64-string
            # Credits to Willem Van Onsem, https://stackoverflow.com/questions/52444818/how-to-convert-a-png-image-to-string-and-send-it-through-django-api
            encoded_image = base64.b64encode(img_file.read()).decode()

            data["post_id"] = new_id
            data["content"] = str(encoded_image)
            data["contentType"] = content_type

            serializer = PostsSerializer(data=data)
            serializer.is_valid()
            serializer.save()

    return success, message, post_serializer.data


def handle_posts(request):
    query = request.data["query"]
    success = False
    message = "Post not created"

    success, message, new_post = create_post(request)

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