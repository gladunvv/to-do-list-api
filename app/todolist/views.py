from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from todolist.models import ToDoList, Item, Marker
from todolist.serializers import (
    ToDoListSerializer,
    CreateToDoListSerializer,
)

class ToDoListView(APIView):

    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        
        user = request.user
        to_do_list = get_list_or_404(ToDoList, user=user)
        serializer = ToDoListSerializer(to_do_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class OneToDoListView(APIView):

    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, pk, *args, **kwargs):

        user = request.user
        to_do = get_object_or_404(ToDoList, user=user, pk=pk)
        serializer = ToDoListSerializer(to_do)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CreateToDoListView(APIView):

    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        user = request.user
        data = request.data
        serializer = CreateToDoListSerializer(data=data)
        if serializer.is_valid():
            serializer.save(user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)