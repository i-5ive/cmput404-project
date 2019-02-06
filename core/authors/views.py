from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets

from core.authors.models import Author
from core.authors.serializers import AuthorSerializer


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
