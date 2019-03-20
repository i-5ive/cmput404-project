import logging

from django.core.paginator import Paginator
# Create your views here.
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from core.authors.models import Follow
from core.authors.util import get_author_id
from core.posts.constants import DEFAULT_POST_PAGE_SIZE
from core.posts.create_posts_view import handle_posts
from core.posts.models import Posts, Comments
from core.posts.serializers import PostsSerializer, CommentsSerializer
from core.posts.util import can_user_view, add_page_details_to_response

logger = logging.getLogger(__name__)

COMMENT_NOT_ALLOWED = 'Comment not allowed'
COMMENT_ADDED = 'Comment Added'


def create_comment(request, pk=None):
    post = Posts.objects.get(pk=pk)
    if post:
        data = request.data
        print(data)
        comment = data.get('comment', None)
        author = comment.get('author', None)
        author_id = author['id'].rstrip('/').split('/')[-1]
        comment['author'] = author_id
        serializer = CommentsSerializer(data=comment)
        if serializer.is_valid():
            post.comments.create(**serializer.validated_data)
            return Response({
                "query": "addComment",
                "success": True,
                "message": COMMENT_ADDED
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "query": "addComment",
                "success": False,
                "message": COMMENT_NOT_ALLOWED,
                "errors": serializer.errors
            }, status=status.HTTP_403_FORBIDDEN)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


def list_comments(request, pk=None):
    size = int(request.query_params.get("size", 5))
    queryPage = int(request.query_params.get('page', 0))
    if size < 1 or queryPage < 0 or size > 100:
        return Response({
            "success": False,
            "message": "The query parameters were invalid",
            "query": "comments"
        }, 400)

    post = Posts.objects.get(pk=pk)
    if not can_user_view(request.user, post):
        return Response({
            "success": False,
            "message": "You are not authorized to view this post's comments.",
            "query": "comments"
        }, status=401)

    comments = Comments.objects.filter(post=post)

    try:
        paginator = Paginator(comments, size)
        page = paginator.page(queryPage + 1)
        serializer = CommentsSerializer(page, many=True, context={'request': request})
        comments_to_return = serializer.data
    except:
        comments_to_return = []

    data = {
        "comments": comments_to_return,
        "query": "comments",
        "count": len(comments),
        "size": size
    }
    if (len(comments_to_return) > 0):
        add_page_details_to_response(request, data, page, queryPage)

    return Response(data)


class PostsViewSet(viewsets.ModelViewSet):
    queryset = Posts.objects.filter(visibility="PUBLIC").order_by('-published')
    serializer_class = PostsSerializer

    def retrieve(self, request, *args, **kwargs):
        post = self.get_object()
        if not can_user_view(request.user, post):
            return Response({
                "success": False,
                "message": "You are not authorized to view this post.",
                "query": "post"
            }, status=401)
        posts = Posts.objects.filter(post_id=post.post_id)
        serializer = PostsSerializer(posts, many=True, context={'request': request})
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        size = int(request.query_params.get("size", 5))
        queryPage = int(request.query_params.get('page', 0))
        if size < 1 or queryPage < 0 or size > 100:
            return Response({
                "success": False,
                "message": "The query parameters were invalid",
                "query": "posts"
            }, 400)

        try:
            qs_posts = self.get_queryset().exclude(unlisted=True)
            paginator = Paginator(qs_posts, size)
            page = paginator.page(queryPage + 1)
            serializer = self.get_serializer(page, many=True)
            pages_to_return = serializer.data
        except:
            pages_to_return = []

        data = {
            "posts": pages_to_return,
            "query": "posts",
            "count": len(qs_posts),
            "size": size
        }
        if len(pages_to_return) > 0:
            add_page_details_to_response(request, data, page, queryPage)

        return Response(data)

    @action(detail=True, url_path='comments', methods=["GET", "POST"])
    def comments(self, request, pk=None):
        if request.method == "GET":
            return list_comments(request, pk=pk)
        elif request.method == "POST":
            return create_comment(request, pk=pk)
        else:
            Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def create(self, request, **kwargs):
        return handle_posts(request)

    def destroy(self, request, pk=None, **kwargs):
        # Use post_id to delete all related image posts too
        post = Posts.objects.get(pk=pk)
        if (not request.user.is_authenticated) or request.user.author != post.author:
            return Response({
                "success": False,
                "message": "You must be logged in as the author of the post to delete it.",
                "query": "deletePost"
            }, status=401)

        Posts.objects.filter(post_id=post.post_id).delete()
        return Response({
            "success": True,
            "message": "Post deleted successfully",
            "query": "deletePost"
        }, status=200)

    @action(methods=['get'], detail=False, url_path='feed', url_name='home_feed')
    def get_home_feed(self, request):
        size = int(request.query_params.get("size", DEFAULT_POST_PAGE_SIZE))
        queryPage = int(request.query_params.get('page', 0))
        if size < 1 or queryPage < 0 or size > 100:
            return Response({
                "success": False,
                "message": "The query parameters were invalid",
                "query": "homeFeed"
            }, 400)

        posts = Posts.objects.filter()
        if request.user.is_authenticated:
            requester_url = request.user.author.get_url()

            posts = Posts.objects.filter(author=request.user.author, unlisted=False)
            followed = Follow.objects.filter(follower=requester_url)
            followedIds = []
            for follow in followed:
                followedIds.append(get_author_id(follow.followed))
            posts |= Posts.objects.filter(author__id__in=followedIds, unlisted=False).exclude(visibility="PRIVATE")
            posts |= Posts.objects.filter(author__id__in=followedIds, unlisted=False, visibility="PRIVATE",
                                          visibleTo__contains=[requester_url])
        else:
            posts = Posts.objects.filter(visibility__in=["PUBLIC", "SERVERONLY"], unlisted=False)

        paginator = Paginator(posts, size)
        try:
            page = paginator.page(queryPage + 1)
            serializer = PostsSerializer(page, many=True, context={'request': request})
            posts_to_return = serializer.data
        except:
            posts_to_return = []

        data = {
            "query": "homeFeed",
            "success": True,
            "posts": posts_to_return,
            "count": len(posts),
            "size": size
        }
        if len(posts_to_return) > 0:
            add_page_details_to_response(request, data, page, queryPage)
        return Response(data)
