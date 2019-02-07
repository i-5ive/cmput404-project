"""
Things to test

- CRUD Account
- GET another account
- LIST accounts
- Update account (PATCH)
- Account already exists
- Invalid data
"""
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIRequestFactory, APITestCase, force_authenticate

from core.users.views import UserViewSet

NUM_USERS = 5
User = get_user_model()


class GetAllUsersTestCase(APITestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.admin = User.objects.create(username='admin', email='admin@admin.com', password='AdminPaSsWord!',
                                         is_superuser=True)

        for i in range(0, NUM_USERS):
            User.objects.create(username='test{}'.format(i), email='test{}@example.com'.format(i), password='test1234')

    def test_get_all_users_as_admin(self):
        view = UserViewSet.as_view({'get': 'list'})
        request = self.factory.get(reverse('users-list'))
        force_authenticate(request, user=self.admin)
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), NUM_USERS + 1)  # add one for admin :D

    def test_get_all_users_as_anon(self):
        view = UserViewSet.as_view({'get': 'list'})
        request = self.factory.get(reverse('users-list'))
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # 200 OK since and empty list is returned.
        self.assertEqual(len(response.data), 0)

    def test_get_all_users_as_user(self):
        view = UserViewSet.as_view({'get': 'list'})
        request = self.factory.get(reverse('users-list'))
        force_authenticate(request, user=get_user_model().objects.get(pk=2))
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # should just be me :D
