from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.core import exceptions


TDL_ONE_URL = reverse('todolist:tdl_one', kwargs={'pk': 1})
TDL_ALL_URL = reverse('todolist:tdl_all')
TDL_CREATE_URL = reverse('todolist:tdl_create')
ITEM_CREATE_URL = reverse('todolist:item_create', kwargs={'pk': 1})
ITEM_UPDATE_URL = reverse('todolist:item_update',
                          kwargs={
                              'tdl_pk': 1,
                              'it_pk': 1,
                          })
MK_ALL_URL = reverse('todolist:mk_all')
MK_CREATE_URL = reverse('todolist:mk_create')

CREATE_USER_URL = reverse('user:createuser')


class ToDoListTests(TestCase):

    def setUp(self):
        self.client = APIClient()

    def token_user(self):
        context = {
            'username': 'newuser',
            'email': 'test@bounty.com',
            'password': 'newpass1234',
        }
        self.client.post(CREATE_USER_URL, context)
        user = get_user_model().objects.get(username=context['username'])
        token = user.auth_token
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    def create_tdl(self):
        context = {
            'name': 'new_tdl'
        }
        self.token_user()
        self.client.post(TDL_CREATE_URL, context)

    def test_create_tdl(self):
        context = {
            'name': 'new_tdl',
        }
        self.token_user()
        res = self.client.post(TDL_CREATE_URL, context)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_view_all_tdl(self):
        self.token_user()
        self.create_tdl()
        res = self.client.get(TDL_ALL_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_view_one_tdl(self):
        self.token_user()
        self.create_tdl()
        res = self.client.get(TDL_ONE_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_item(self):
        context = {
            'title': 'new_item',
            'todo_list': 1,
        }
        self.create_tdl()
        self.token_user()
        res = self.client.post(ITEM_CREATE_URL, context)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data['title'], context['title'])

    def test_update_item(self):
        context_old = {
            'title': 'old_item',
            'todo_list': 1,
        }
        context_new = {
            'title': 'new_item'
        }
        self.create_tdl()
        self.token_user()
        self.client.post(ITEM_CREATE_URL, context_old)
        res = self.client.patch(ITEM_UPDATE_URL, context_new)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertNotEqual(res.data['title'], context_old['title'])

    def test_create_mk_url(self):
        context = {
            'name': 'new_mk'
        }
        self.create_tdl()
        self.token_user()
        res = self.client.post(MK_CREATE_URL, context)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_view_mk_all(self):
        context = {
            'name': 'new_mk'
        }
        self.create_tdl()
        self.token_user()
        self.client.post(MK_CREATE_URL, context)
        res = self.client.get(MK_ALL_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)