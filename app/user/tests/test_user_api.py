from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:createuser')
LOGIN_USER_URL = reverse('user:login')
VERIFICATION_USER_URL = reverse('user:verification')
LOGOUT_USER_URL = reverse('user:logout')
DELETE_USER_URL = reverse('user:delete')


def create_user(*args, **kwargs):
    return get_user_model().objects.create_user(**kwargs)


class UserApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_create_user_success(self):
        context = {
            'username': 'newuser',
            'email': 'test@bounty.com',
            'password': 'newpass1234',
        }

        res = self.client.post(CREATE_USER_URL, context)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_create_user_exists_bed_password(self):
        context = {
            'username': 'newuser',
            'email': 'test@bounty.com',
            'password': 'newpass',
        }

        res = self.client.post(CREATE_USER_URL, context)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_exists_bad_email(self):
        context = {
            'username': 'newuser',
            'email': 'testbad',
            'password': 'newpass1234',
        }
        res = self.client.post(CREATE_USER_URL, context)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_user(self):
        context = {
            'username': 'newuser',
            'email': 'test@bounty.com',
            'password': 'newpass1234',
        }
        create_user(**context)
        res = self.client.post(LOGIN_USER_URL, context)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_for_user(self):
        context = {
            'username': 'newuser',
            'email': 'test@bounty.com',
            'password': 'newpass1234',
        }
        res = self.client.post(CREATE_USER_URL, context)
        self.assertIn('token', res.data)

