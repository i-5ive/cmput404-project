# Create your views here.
from django.contrib.auth import get_user_model
from rest_framework import viewsets, permissions

from .serializers import UserSerializer

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)

    def get_queryset(self):
        """
        If the user is an admin, they can get all users, otherwise only their specific User object will be returned
        https://stackoverflow.com/a/22767325 - argaen 2019/02/06
        :return:
        """
        if self.request.user.is_superuser:
            return User.objects.all()
        else:
            return User.objects.filter(id=self.request.user.id)
