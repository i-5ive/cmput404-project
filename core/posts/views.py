from django.shortcuts import render
from django.core.paginator import Paginator

# Create your views here.
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from core.posts.models import Posts, Comments
from core.posts.serializers import PostsSerializer, CommentsSerializer
from core.posts.create_posts_view import handle_posts
from core.posts.util import can_user_view, add_page_details_to_response
from core.posts.constants import DEFAULT_POST_PAGE_SIZE
from core.authors.models import Follow
from core.authors.util import get_author_id

import logging

logger = logging.getLogger(__name__)


class PostsViewSet(viewsets.ModelViewSet):
    queryset = Posts.objects.filter(visibility="PUBLIC").order_by('-published')
    serializer_class = PostsSerializer

    def retrieve(self, request, pk):
        post = Posts.objects.get(pk=pk)
        if (not can_user_view(request.user, post)):
            return Response({
                "success": False,
                "message": "You are not authorized to view this post.",
                "query": "post"
            }, status=401)
        posts = Posts.objects.filter(post_id=post.post_id)
        serializer = PostsSerializer(posts, many=True, context={'request': request})
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        posts = self.get_queryset().exclude(unlisted=True)
        page = self.paginate_queryset(posts)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data)

    @action(detail=True)
    def comments(self, request, pk):
        size = int(request.query_params.get("size", 5))
        queryPage = int(request.query_params.get('page', 0))
        if (size < 1 or queryPage < 0 or size > 100):
            return Response({
                "success": False,
                "message": "The query parameters were invalid",
                "query": "comments"
            }, 400)
        
        post = Posts.objects.get(pk=pk)
        if (not can_user_view(request.user, post)):
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

    def create(self, request, **kwargs):
        return handle_posts(request)

    def destroy(self, request, pk=None, **kwargs):
        # Use post_id to delete all related image posts too
        post = Posts.objects.get(pk=pk)
        if ((not request.user.is_authenticated) or request.user.author != post.author):
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
        if (size < 1 or queryPage < 0 or size > 100):
            return Response({
                "success": False,
                "message": "The query parameters were invalid",
                "query": "homeFeed"
            }, 400)
        
        posts = Posts.objects.filter()
        if (request.user.is_authenticated):
            requester_url = request.user.author.get_url()
            
            posts = Posts.objects.filter(author=request.user.author, unlisted=False)
            followed = Follow.objects.filter(follower=requester_url)
            followedIds = []
            for follow in followed:
                followedIds.append(get_author_id(follow.followed))
            posts |= Posts.objects.filter(author__id__in=followedIds, unlisted=False).exclude(visibility="PRIVATE")
            posts |= Posts.objects.filter(author__id__in=followedIds, unlisted=False, visibility="PRIVATE", visibleTo__contains=[requester_url])
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
        if (len(posts_to_return) > 0):
            add_page_details_to_response(request, data, page, queryPage)
        return Response(data)
