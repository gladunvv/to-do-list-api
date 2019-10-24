from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from todolist.models import (
    Marker,
    ToDoList,
    Item
)

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
        return user

    def create_tdl(self):
        context = {
            'name': 'new_tdl'
        }
        self.token_user()
        self.client.post(TDL_CREATE_URL, context)
        tdl = ToDoList.objects.get(pk=1)
        return tdl

    def test_create_tdl(self):
        context = {
            'name': 'new_tdl',
        }
        self.token_user()
        res = self.client.post(TDL_CREATE_URL, context)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_tdl_models_str_method(self):
        user = self.token_user()
        tdl = ToDoList.objects.create(
            name='Test ITEM',
            user=user)
        self.assertEqual(str(tdl), 'Test ITEM')

    def test_create_tdl_bad_request(self):
        context = {
            'fake': 'fake_name'
        }
        self.token_user()
        res = self.client.post(TDL_CREATE_URL, context)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

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
        }
        self.create_tdl()
        self.token_user()
        res = self.client.post(ITEM_CREATE_URL, context)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data['title'], context['title'])

    def test_item_models_str_method(self):
        self.token_user()
        tdl = self.create_tdl()
        item = Item.objects.create(
            title='Test ITEM',
            todo_list=tdl,
        )
        self.assertEqual(str(item), 'Test ITEM')

    def test_create_item_bad_request(self):
        context = {
            'fake': 'bad_name',
        }
        self.create_tdl()
        res = self.client.post(ITEM_CREATE_URL, context)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_item(self):
        context_old = {
            'title': 'old_item',
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

    def test_update_item_bad_request(self):
        context_old = {
            'title': 'old_item',
        }
        context_new = {
            'fake': 'new_item'
        }
        self.create_tdl()
        self.token_user()
        self.client.post(ITEM_CREATE_URL, context_old)
        res = self.client.patch(ITEM_UPDATE_URL, context_new)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_mk_url(self):
        context = {
            'name': 'new_mk'
        }
        self.token_user()
        self.create_tdl()
        res = self.client.post(MK_CREATE_URL, context)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_mk_models_str_method(self):
        user = self.token_user()
        marker = Marker.objects.create(
            name='Test MK',
            user=user)
        self.assertEqual(str(marker), 'Test MK')

    def test_create_mk_url_bad_request(self):
        context = {
            'bad': 'bad_name'
        }
        self.create_tdl()
        self.token_user()
        res = self.client.post(MK_CREATE_URL, context)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_view_mk_all(self):
        context = {
            'name': 'new_mk'
        }
        self.create_tdl()
        self.token_user()
        self.client.post(MK_CREATE_URL, context)
        res = self.client.get(MK_ALL_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
