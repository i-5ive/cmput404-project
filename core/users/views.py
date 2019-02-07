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


        EXCERPT FROM: https://stackoverflow.com/a/22767325 - argaen 2019/02/06
        Customizing the get_queryset method this way means the following:

        Yes, non-authenticated users can send the GET request to retrieve the user list but it will be empty because
        the return User.objects.filter(id=self.request.user.id) ensures that only information about the authenticated
        user is returned.

        The same applies for other methods, if an authenticated user tries to DELETE another user object, a
        detail: Not found will be returned (because the user it is trying to access is not in the queryset).

        Authenticated users can do whatever they want to their user objects.`
        :return:
        """
        if self.request.user.is_superuser:
            return User.objects.all()
        else:
            return User.objects.filter(id=self.request.user.id)
