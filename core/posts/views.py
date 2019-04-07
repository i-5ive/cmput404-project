import logging
import json
import base64

from django.core.paginator import Paginator
# Create your views here.
from rest_framework import viewsets, status
from rest_framework.decorators import action, detail_route
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from django.http import HttpResponse

from core.authors.models import Follow
from core.authors.util import get_author_id, get_author_url
from core.authors.friends_util import are_friends, get_friends
from core.posts.constants import DEFAULT_POST_PAGE_SIZE
from core.posts.create_posts_view import handle_posts
from core.posts.models import Posts, Comments
from core.posts.serializers import PostsSerializer, CommentsSerializer
from core.posts.util import can_user_view, can_external_user_view, add_page_details_to_response, merge_posts_with_github_activity, merge_posts

from core.github_util import get_github_activity

from core.servers.SafeServerUtil import ServerUtil
from core.hostUtil import is_external_host

logger = logging.getLogger(__name__)

COMMENT_NOT_ALLOWED = 'You are not allowed to comment on this post'
COMMENT_ADDED = 'Your comment has been added'
POST_NOT_VISIBLE = "This post is not visible to the current user"

def create_comment(request, pk=None):
    post = get_object_or_404(Posts, pk=pk)
    
    is_server = ServerUtil.is_server(request.user)
    
    if (not is_server and not can_user_view(request.user, post)):
        return Response(status=status.HTTP_403_FORBIDDEN)
    if post:
        data = request.data
        comment = data.get("comment", None)
        if (isinstance(comment, str)):
            comment = json.loads(comment)
        author = comment.get('author', None)
        author_id = author['id']
        try:
            su = ServerUtil(authorUrl=author_id)
            if (is_server and not (su.is_valid() and su.should_share_posts() and can_external_user_view(author_id, post))):
                return Response({
                    "query": "addComment",
                    "success": False,
                    "message": POST_NOT_VISIBLE,
                }, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            print(e)
            return Response({
                "query": "addComment",
                "success": False,
                "message": POST_NOT_VISIBLE,
            }, status=status.HTTP_403_FORBIDDEN)
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
        }, status=status.HTTP_400_BAD_REQUEST)

    post = get_object_or_404(Posts, pk=pk)
    if not can_user_view(request.user, post):
        return Response({
            "success": False,
            "message": "You are not authorized to view this post's comments.",
            "query": "comments"
        }, status=status.HTTP_403_FORBIDDEN)

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

    def retrieve(self, request, pk):
        print("PostsViewSet retrieve:", request, pk)
        if ServerUtil.is_server(request.user):
            xUser = request.META.get("HTTP_X_REQUEST_USER_ID")
            if not xUser:
                return Response("Foreign node failed to provide required X-Header.", status=400)
            data = {
                "author": {
                    "url": xUser
                }
            }
            return self.__do_a_get_post(request.user, data, pk)
        try:
            post = Posts.objects.get(pk=pk)
        except:
            return Response({
                "success": False,
                "message": "No post was found with that ID",
                "query": "post"
            }, status=404)
        if not can_user_view(request.user, post):
            return Response({
                "success": False,
                "message": "You are not authorized to view this post.",
                "query": "post"
            }, status=status.HTTP_403_FORBIDDEN)
        serializer = PostsSerializer(post, context={'request': request})
        return Response({
            "query": "posts",
            "count": 1,
            "size": 1,
            "posts": [serializer.data]
        })

    @action(detail=True, url_path='image', methods=["GET"])
    def image(self, request, pk):
        try:
            post = Posts.objects.get(pk=pk)
        except:
            return Response({
                "success": False,
                "message": "No post was found with that ID",
                "query": "getImage"
            }, status=404)
        if not can_user_view(request.user, post):
            return Response({
                "success": False,
                "message": "You are not authorized to view this post.",
                "query": "post"
            }, status=status.HTTP_403_FORBIDDEN)
        if (post.visibility == "PUBLIC"):
            if ("," in post.content):
                data = post.content.split(",")[1]
            else:
                data = post.content
            data = data.encode()
            data = base64.b64decode(data)
        else:
            data = post.content
        return HttpResponse(data, content_type=post.contentType.split(";")[0])

    def update(self, request, pk):
        try:
            post = Posts.objects.get(pk=pk)
        except:
            return Response({
                "success": False,
                "message": "No post was found with that ID",
                "query": "updatePost"
            }, status=404)
        
        if ((not request.user.is_authenticated) or request.user.author != post.author):
            return Response({
                "success": False,
                "message": "You are not authorized to edit this post.",
                "query": "updatePost"
            }, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, pk)
    
    def list(self, request, *args, **kwargs):
        print("hit posts list endpoint:", request, args, kwargs)
        size = int(request.query_params.get("size", 5))
        queryPage = int(request.query_params.get('page', 0))
        if size < 1 or queryPage < 0 or size > 100:
            return Response({
                "success": False,
                "message": "The query parameters were invalid",
                "query": "posts"
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            qs_posts = self.get_queryset().exclude(unlisted=True)
            paginator = Paginator(qs_posts, size)
            page = paginator.page(queryPage + 1)
            serializer = self.get_serializer(page, many=True)
            pages_to_return = serializer.data
        except Exception as e:
            print(e)
            pages_to_return = []

        data = {
            "posts": pages_to_return,
            "query": "posts",
            "count": len(qs_posts),
            "size": size
        }
        if len(pages_to_return) > 0:
            add_page_details_to_response(request, data, page, queryPage)
        return Response(data, status=200)

    def __do_a_get_post(self, user, data, pk):
        try:
            post = Posts.objects.get(pk=pk)
        except:
            return Response({
                "success": False,
                "message": "No post was found with that ID",
                "query": "getPost"
            }, status=404)

        visibility = post.visibility
        requestingAuthorUrl = data.get("author", {}).get("url", None)
        if not requestingAuthorUrl:
            return Response("You must specify the URL of the author who is requesting the post.", status=400)
        postAuthorUrl = get_author_url(str(post.author.pk))

        sUtil = ServerUtil(authorUrl=requestingAuthorUrl)
        if not sUtil.is_valid():
            return Response("Could not find a foreign node matching the reqesting author's url.", status=400)

        # TODO block pictures or posts based on content type
        if not sUtil.should_share_posts():
            return Response("This node is currently not sharing posts with the requesting foreign node.", status=400)

        if visibility == "PUBLIC":
            serializer = PostsSerializer(post)
            return Response({
                "query": "posts",
                "count": 1,
                "size": 1,
                "posts": [serializer.data]
            })
        
        # If they are direct friends they can still see a FOAF post
        if visibility == "FRIENDS" or visibility == "FOAF":
            local, remote_follow = are_friends(postAuthorUrl, requestingAuthorUrl)
            success, remote = sUtil.check_direct_friendship(requestingAuthorUrl, postAuthorUrl)

            if not success:
                return Response("Failed to communicate with external server to check friendship.", status=500)
            if not remote:
                remote_follow.delete()
            elif local: # remote = true, local = true, can respond with post
                return Response({
                    "query": "posts",
                    "count": 1,
                    "size": 1,
                    "posts": [serializer.data]
                })

        # If we reach here, we know that they are not direct friends
        # We need to find all the friends of the post writer
        # and then ask the remote server if any of those friends are friends with the requesting author
        if visibility == "FOAF":
            postAuthorFriends = get_friends(postAuthorUrl)
            success, foafs = sUtil.check_at_least_one_friend(requestingAuthorUrl, postAuthorFriends)

            if not success:
                return Response("Failed to communicate with external server to check foaf-ship.", status=500)

            if foafs:
                return Response({
                    "query": "posts",
                    "count": 1,
                    "size": 1,
                    "posts": [serializer.data]
                })

        if visibility == "PRIVATE":
            print("UGHHH")

        return Response({
            "query": "posts",
            "count": 0,
            "size": 1,
            "posts": []
        })


    # For FOAF, test you can actually hand out a post
    def post(self, request, pk):
        user = request.user
        data = request.data

        if not user.is_authenticated or not ServerUtil.is_server(user):
            return Response("You must be authenticated as a foreign node to access this endpoint.", status=401)

        query = request.data.get("query", False)
        if not query and not query == "getPost":
            return Response("This endpoint only accepts the 'getPost' query type.", status=400)

        if not data.get("postid", "") == pk or not data.get("url", "").endswith(pk):
            return Response("You must ensure that the post IDs and urls match.", status=400)

        return self.__do_a_get_post(user, data, pk)

    @action(detail=True, url_path='comments', methods=["GET", "POST"])
    def comments(self, request, pk=None):
        print(request)
        if request.method == "GET":
            return list_comments(request, pk=pk)
        elif ServerUtil.is_server(request.user):
            print("This is a server")
            xUser = request.META.get("HTTP_X_REQUEST_USER_ID")
            postUrl = request.data.get("post", None)
            if not postUrl:
                return Response("You failed to specify the 'post' of the query.", 400)
            pk = postUrl.split("posts/")[1]
            post = get_object_or_404(Posts, pk=pk)
            commentData = request.data.get("comment", {})
            authorData = commentData.get("author", {})
            authorUrl = authorData.get("id", None)
            if not authorUrl:
                return Response("You failed to specify the author's id.", 400)
            serializer = CommentsSerializer(data=commentData)
            commentData['author'] = authorUrl
            if serializer.is_valid():
                post.comments.create(**serializer.validated_data)
                return Response("It's created hopefully", 200)
            else:
                return Response("Some error who knows", 400)
        elif request.method == "POST":
            return create_comment(request, pk=pk)
        else:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @action(detail=True, url_path='update', methods=["POST"])
    def update_post(self, request, pk=None):
        try:
            post = Posts.objects.get(pk=pk)
            if (post.author != request.user.author):
                return Response({
                    "query": "updatePost",
                    "success": False,
                    "message": "You must be authenticated to update a post"
                }, status=status.HTTP_403_FORBIDDEN)
            Posts.objects.filter(pk=pk).update(**json.loads(request.data["postData"]))
            return Response({
                "query": "updatePost",
                "success": True,
                "message": "Your post has been updated."
            })
        except Exception as e:
            return Response({
                "query": "updatePost",
                "success": False,
                "message": str(e)
            }, status=400)
            
    @action(detail=False, url_path='createExternalComment', methods=["POST"])
    def create_external_comment(self, request):
        if (not request.user.is_authenticated):
            return Response({
                "query": "createExternalComment",
                "message": "You must be authenticated",
                "success": False
            }, status=403)
        try:
            postUrl = request.data["postUrl"]
            authorUrl = get_author_url(str(request.user.author.pk))
            sUtil = ServerUtil(postUrl=postUrl)
            if not sUtil.is_valid():
                return Response("No foreign node with the base url: "+postUrl, status=404)
                
            data = request.data
            comment = data.get("comment", None)
            if (isinstance(comment, str)):
                comment = json.loads(comment)
            
            success, res = sUtil.create_comment(postUrl.split("/posts/")[1], authorUrl, comment, postUrl)
            if not success:
                return Response("Failed to post foreign comment: "+postUrl, status=500)
            return Response(res)
        except Exception as e:
            print(e)
            return Response({
                "query": "createExternalComment",
                "message": e,
                "success": False
            }, status=400)
    
    def create(self, request, **kwargs):
        return handle_posts(request)

    def destroy(self, request, pk=None, **kwargs):
        # Use post_id to delete all related image posts too
        try:
            post = Posts.objects.get(pk=pk)
        except:
            return Response({
                "success": False,
                "message": "No post was found with that ID",
                "query": "deletePost"
            }, status=404)
        if (not request.user.is_authenticated) or request.user.author != post.author:
            return Response({
                "success": False,
                "message": "You must be logged in as the author of the post to delete it.",
                "query": "deletePost"
            }, status=status.HTTP_403_FORBIDDEN)
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

        if request.user.is_authenticated:
            requester_url = request.user.author.get_url()

            posts = Posts.objects.filter(author=request.user.author, unlisted=False)
            followed = Follow.objects.filter(follower=requester_url)
            localFollowedIds = []
            externalPosts = []
            for follow in followed:
                if (is_external_host(follow.followed)):
                    external_host_url = follow.followed.split("/author/")[0]
                    sUtil = ServerUtil(authorUrl=external_host_url)
                    if not sUtil.valid_server():
                        print("authorUrl found, but not in DB", external_host_url)
                        continue # We couldn't find a server that matches the friend URL base
                    # split the id from the URL and ask the external server about them
                    success, fetched_posts = sUtil.get_posts_by_author(follow.followed.split("/author/")[1], requester_url)
                    if not success:
                        continue # We couldn't successfully fetch from an external server

                    externalPosts += fetched_posts["posts"]
                else:
                    localFollowedIds.append(get_author_id(follow.followed))
            posts |= Posts.objects.filter(author__id__in=localFollowedIds, unlisted=False).exclude(visibility="PRIVATE")
            posts |= Posts.objects.filter(author__id__in=localFollowedIds, unlisted=False, visibility="PRIVATE",
                                          visibleTo__contains=[requester_url])
            viewable_posts = []
            for post in posts:
                if (can_user_view(request.user, post)):
                    viewable_posts.append(post)

            github_stream = get_github_activity(request.user.author)
            posts = merge_posts_with_github_activity(viewable_posts, github_stream)
        else:
            posts = Posts.objects.filter(visibility__in=["PUBLIC"], unlisted=False)
            externalPosts = []
        
        try:
            # don't look at this
            if (len(externalPosts) > 0):
                serializer = PostsSerializer(posts, many=True, context={'request': request})
                posts_to_return = serializer.data
                
                sorted_posts = sorted(externalPosts + posts_to_return, key=lambda x : x["published"], reverse=True)
                paginator = Paginator(sorted_posts, size)
                page = paginator.page(queryPage + 1)
                posts_to_return = page.object_list
            else:
                paginator = Paginator(posts, size)
                page = paginator.page(queryPage + 1)
                serializer = PostsSerializer(page, many=True, context={'request': request})
                posts_to_return = serializer.data

        except Exception as e:
            print(e)
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

    # get the latest posts from external servers
    # or, if post url specified, fetch that post specifically 
    @action(methods=['get'], detail=False, url_path='external')
    def get_external_posts(self, request):
        print("get_external_posts endpoint:", request)
        user = request.user
        if ServerUtil.is_server(user):
            return Response("Foreign Nodes may not grab posts from this endpoint.", status=401)

        postUrl = request.query_params.get("postUrl", False)
        if postUrl:
            authorUrl = get_author_url(str(request.user.author.pk)) if request.user.is_authenticated else ""
            sUtil = ServerUtil(postUrl=postUrl)
            if not sUtil.is_valid():
                return Response("No foreign node with the base url: "+postUrl, status=404)
            success, post = sUtil.get_post(postUrl.split("/posts/")[1], authorUrl)
            if not success:
                return Response("Failed to grab foreign post: "+postUrl, status=500)
            return Response(post)
        posts = ServerUtil.get_external_posts_aggregate()
        return Response({"posts":posts})