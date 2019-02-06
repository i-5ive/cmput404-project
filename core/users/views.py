# Create your views here.
from rest_framework import viewsets

from core.users.models import Author
from core.users.serializers import AuthorSerializer


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
