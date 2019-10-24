from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from todolist.models import ToDoList, Item, Marker
from todolist.serializers import (
    ItemSerializer,
    ToDoListSerializer,
    CreateToDoListSerializer,
    MarkerSerializer,
    CreateMarkerSerializer,
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


class CreateItemView(APIView):

    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, pk, *args, **kwargs):
        todo_list = get_object_or_404(ToDoList, pk=pk)
        data = request.data
        serializer = ItemSerializer(data=data)
        if serializer.is_valid():
            serializer.save(todo_list=todo_list)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateItemView(APIView):

    permission_classes = (permissions.IsAuthenticated,)

    def patch(self, request, tdl_pk, it_pk, *args, **kwargs):
        item = get_object_or_404(Item, todo_list=tdl_pk, pk=it_pk)
        data = request.data
        serializer = ItemSerializer(item, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MarkerView(APIView):

    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        user = request.user
        markers = get_list_or_404(Marker, user=user)
        serializer = MarkerSerializer(markers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CreateMarker(APIView):

    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        user = request.user
        data = request.data
        serializer = CreateMarkerSerializer(data=data)
        if serializer.is_valid():
            serializer.save(user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
