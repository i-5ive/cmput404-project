from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets

from core.posts.models import Posts
from core.posts.serializers import PostsSerializer


class PostsViewSet(viewsets.ModelViewSet):
    queryset = Posts.objects.all()
    serializer_class = PostsSerializer