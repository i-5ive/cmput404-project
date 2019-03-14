from django.shortcuts import render
from django.core.paginator import Paginator

# Create your views here.
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from core.posts.models import Posts, Comments
from core.posts.serializers import PostsSerializer, CommentsSerializer
from core.posts.posts_view import handle_posts as handle_posts

import logging

logger = logging.getLogger(__name__)


class PostsViewSet(viewsets.ModelViewSet):
    queryset = Posts.objects.filter(visibility="PUBLIC").order_by('-published')
    serializer_class = PostsSerializer

    def retrieve(self, request, *args, **kwargs):
        post = self.get_object()
        posts = Posts.objects.filter(post_id=post.post_id)
        serializer = PostsSerializer(posts, many=True, context={'request': request})
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            posts = self.get_queryset()
        else:
            posts = self.get_queryset().exclude(contentType__contains='image')

        page = self.paginate_queryset(posts)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data)

    @action(detail=True)
    def comments(self, request, pk):
        post = self.get_object()
        comments = Comments.objects.filter(post=post)
        paginator = Paginator(comments, 5)
        page= request.query_params.get('page', 1)
        serializer = CommentsSerializer(paginator.page(page), many=True, context={'request': request})
        return Response(serializer.data)

    def create(self, request, **kwargs):
        return handle_posts(request)

    def destroy(self, request, pk=None, **kwargs):
        # Use post_id to delete all related image posts too
        post = self.get_object()
        Posts.objects.filter(post_id=post.post_id).delete()
        return Response({
            "success": True,
            "message": "Post deleted successfully"
        }, status=200)



    

