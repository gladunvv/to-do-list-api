from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from todolist.models import ToDoList, Item, Marker
from todolist.serializers import ToDoListSerializer

class ToDoListView(APIView):

    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        
        user = request.user
        to_do_list = get_list_or_404(ToDoList, user=user)
        serializer = ToDoListSerializer(to_do_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
