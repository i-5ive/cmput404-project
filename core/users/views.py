# Create your views here.
from django.contrib.auth import get_user_model  # If used custom user model
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.generics import CreateAPIView

from core.users.models import User
from .serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CreateUserView(CreateAPIView):
    model = get_user_model()
    permission_classes = [
        permissions.AllowAny  # Or anon users can't register
    ]
    serializer_class = UserSerializer
