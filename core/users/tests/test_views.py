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

from core.authors.models import Author
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
        self.assertEqual(response.data["count"], NUM_USERS + 1)  # add one for admin :D

    def test_get_all_users_as_anon(self):
        view = UserViewSet.as_view({'get': 'list'})
        request = self.factory.get(reverse('users-list'))
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # 200 OK since and empty list is returned.
        self.assertEqual(response.data["count"], 0)

    def test_get_all_users_as_user(self):
        view = UserViewSet.as_view({'get': 'list'})
        request = self.factory.get(reverse('users-list'))
        force_authenticate(request, user=get_user_model().objects.get(username="test2"))
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)  # should just be me :D


class GetDetailUserTestCase(APITestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.admin = User.objects.create(username='admin', email='admin@admin.com', password='AdminPaSsWord!',
                                         is_superuser=True)

        for i in range(0, NUM_USERS):
            User.objects.create(pk=i+1, username='test{}'.format(i), email='test{}@example.com'.format(i), password='test1234')

    def test_get_detail_as_admin(self):
        view = UserViewSet.as_view({'get': 'retrieve'})
        request = self.factory.get(reverse('users-detail', kwargs={'pk': 1}))
        force_authenticate(request, user=self.admin)
        response = view(request, pk=1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'id': 1,
                                         'username': 'test0',
                                         'email': 'test0@example.com',
                                         'first_name': '',
                                         'last_name': ''})

    def test_get_detail_for_me(self):
        view = UserViewSet.as_view({'get': 'retrieve'})
        request = self.factory.get(reverse('users-detail', kwargs={'pk': 1}))
        force_authenticate(request, user=get_user_model().objects.get(pk=1))
        response = view(request, pk=1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'id': 1,
                                         'username': 'test0',
                                         'email': 'test0@example.com',
                                         'first_name': '',
                                         'last_name': ''})

    def test_get_detail_as_anon(self):
        view = UserViewSet.as_view({'get': 'retrieve'})
        request = self.factory.get(reverse('users-detail', kwargs={'pk': 2}))
        response = view(request, pk=2)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CreateUserTestCase(APITestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.admin = User.objects.create(username='admin', email='admin@admin.com', password='AdminPaSsWord!',
                                         is_superuser=True)
        self.minimal_valid_data = {
            "username": "test1",
            "email": "test1@example.com",
            "password": get_user_model().objects.make_random_password()
        }
        self.valid_data = {
            "username": "test1",
            "email": "test1@example.com",
            "password": get_user_model().objects.make_random_password(),
            "first_name": "Test",
            "last_name": "User"
        }
        self.invalid_data = {
            "username": "1",
            "password": "",
            "email": "not valid email"
        }

    def test_create_user_minimal_valid_data(self):
        view = UserViewSet.as_view({'post': 'create'})
        request = self.factory.post(reverse('users-list'), data=self.minimal_valid_data, format='json')
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        for key, value in self.minimal_valid_data.items():
            if key != 'password':
                self.assertEqual(response.data[key], value)
        self.assert_author_created(pk=response.data['id'])

    def test_create_user_valid_data(self):
        view = UserViewSet.as_view({'post': 'create'})
        request = self.factory.post(reverse('users-list'), data=self.valid_data, format='json')
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        for key, value in self.valid_data.items():
            if key != 'password':
                self.assertEqual(response.data[key], value)
        self.assert_author_created(pk=response.data['id'])

    def test_create_user_invalid_data(self):
        view = UserViewSet.as_view({'post': 'create'})
        request = self.factory.post(reverse('users-list'), data=self.invalid_data, format='json')
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def assert_author_created(self, pk=None):
        """
        Assert that an author was created with a specified user
        :param pk:
        :return:
        """
        self.assertIsNotNone(Author.objects.filter(user=pk))
