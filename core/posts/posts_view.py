import base64
import json

from rest_framework.decorators import api_view
from rest_framework.response import Response

from core.posts.models import Posts
from core.authors.models import Author
from core.posts.serializers import PostsSerializer

from core.authors.util import get_author_id
    
def create_post(request):
    success = True
    message = "Post created"

    body = request.data
    data = json.loads(body["postData"])

    serializer = PostsSerializer(data=data)
    serializer.is_valid()
    new_post = serializer.save()

    # if image, make another post with generated post_id
    if (request.FILES):
        # Credits to Justin Voss, https://stackoverflow.com/questions/851336/multiple-files-upload-using-same-input-name-in-django
        for img_file in request.FILES.getlist('imageFiles'):
            new_id = new_post.post_id
            image_type = img_file.content_type
            image_size = img_file.size
            
            if image_type == "image/jpeg" or image_type == "image/png":
                content_type = f"{image_type};base64"
            else:
                return False, "Invalid file type"

            # http://www.learningaboutelectronics.com/Articles/How-to-restrict-the-size-of-file-uploads-with-Python-in-Django.php
            if image_size > 10485760:
                return False, "The maximum file size that can be uploaded is 10MB"

            # Credits to Ykh, https://stackoverflow.com/questions/44489375/django-have-admin-take-image-file-but-store-it-as-a-base64-string
            encoded_image = base64.encodestring(img_file.read())

            data["post_id"] = new_id
            data["content"] = str(encoded_image)
            data["contentType"] = content_type

            serializer = PostsSerializer(data=data)
            serializer.is_valid()
            serializer.save()

    return success, message


def handle_posts(request):
    success = False
    message = "Post not created"

    success, message = create_post(request)

    if success: 
        code = 200
    else:
        code = 400

    return Response({
        "success": success,
        "message": message
    }, status=code)