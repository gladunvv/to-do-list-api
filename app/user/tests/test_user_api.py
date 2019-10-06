from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.core import exceptions

from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

VEREFICATION_EMAIL_URL = reverse('user:verification')
CREATE_USER_URL = reverse('user:createuser')
LOGIN_USER_URL = reverse('user:login')
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

    def test_logout_user(self):
        context = {
            'username': 'newuser',
            'email': 'test@bounty.com',
            'password': 'newpass1234',
        }
        res_create = self.client.post(CREATE_USER_URL, context)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + res_create.data['token'])
        self.assertIn('token', res_create.data)
        get_user_model().objects.get(auth_token=res_create.data['token'])
        res = self.client.post(LOGOUT_USER_URL)
        try:
            get_user_model().objects.get(auth_token=res_create.data['token'])
        except exceptions.ObjectDoesNotExist:
            self.assertTrue(True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_delete_user(self):
        context = {
            'username': 'newuser',
            'email': 'test@bounty.com',
            'password': 'newpass1234',
        }
        res_create = self.client.post(CREATE_USER_URL, context)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + res_create.data['token'])
        res = self.client.delete(DELETE_USER_URL)
        try:
            get_user_model().objects.get(username=res_create.data['username'])
        except exceptions.ObjectDoesNotExist:
            self.assertTrue(True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)


    def verification_email(self):
        context = {
            'username': 'newuser',
            'email': 'test@bounty.com',
            'password': 'newpass1234',
        }
        self.client.post(CREATE_USER_URL, context)

        user = get_user_model().objects.get(username=context['username'])
        token = user.auth_token
        uid = urlsafe_base64_encode(force_bytes(user.pk))

        res = self.client.get(VEREFICATION_EMAIL_URL + 'uid={}&token={}'.format(uid, token.key))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('token', res.data)
