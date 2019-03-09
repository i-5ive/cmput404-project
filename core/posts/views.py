from django.shortcuts import render
from django.core.paginator import Paginator

# Create your views here.
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from core.posts.models import Posts, Comments
from core.posts.serializers import PostsSerializer, CommentsSerializer
from core.posts.posts_view import handle_posts as handle_posts

class PostsViewSet(viewsets.ModelViewSet):
    queryset = Posts.objects.all()
    serializer_class = PostsSerializer

    @action(detail=True)
    def comments(self, request, pk):
        post = self.get_object()
        comments = Comments.objects.filter(post=post)
        paginator = Paginator(comments, 5)
        page= request.query_params.get('page', 1)
        serializer = CommentsSerializer(paginator.page(page), many=True, context={'request': request})
        return Response(serializer.data)
    
    def create(self, request):
        return handle_posts(request)
        
    def destroy(self, request, pk=None):
        # Use post_id to delete all related image posts too
        post = Posts.objects.get(pk=pk)
        Posts.objects.filter(post_id=post.post_id).delete()
        return Response({
            "success": True,
            "message": "Post deleted successfully"
        }, status=200)



    

