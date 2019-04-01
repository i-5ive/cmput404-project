import base64

from django.core.paginator import Paginator
from rest_framework.response import Response

from core.authors.models import Author

from core.posts.constants import DEFAULT_POST_PAGE_SIZE

from core.posts.util import add_page_details_to_response
from core.servers.SafeServerUtil import ServerUtil

def get_external_author_posts(request, encoded_url):
    author_url = base64.urlsafe_b64decode(encoded_url).decode("utf8")
    
    size = int(request.query_params.get("size", DEFAULT_POST_PAGE_SIZE))
    page = int(request.query_params.get('page', 0)) + 1
    if size < 1 or page < 0 or size > 100:
        return Response({
            "success": False,
            "message": "The query parameters were invalid",
            "query": "posts"
        }, 400)
    
    external_host_url = author_url.split("/author/")[0]
    sUtil = ServerUtil(authorUrl=external_host_url)
    if not sUtil.valid_server():
        print("authorUrl found, but not in DB", external_host_url)
        return Response({
            "query": "posts",
            "message": "Could not find server",
            "success": False
        }, 400)
    
    requester_url = request.user.author.get_url() if request.user.is_authenticated else None
    success, fetched_posts = sUtil.get_posts_by_author(author_url.split("/author/")[1], requester_url)
    if not success:
        return Response({
            "query": "posts",
            "message": "Could not fetch posts",
            "success": False
        }, 502)
    
    pages = Paginator(fetched_posts["posts"], size)
    current_page = pages.page(page)
    
    response = {
        "query": "posts",
        "count": pages.count,
        "size": size,
        "posts": current_page.object_list
    }
    add_page_details_to_response(request, response, current_page, page - 1)
    return Response(response, status=200)