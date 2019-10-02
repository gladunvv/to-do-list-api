from rest_framework import serializers
from todolist.models import ToDoList, Item, Marker


class ItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = Item
        fields = ('id', 'title', 'priority', 'complited', 'notification_date', 'created_date')


class ToDoListSerializer(serializers.ModelSerializer):

    items = ItemSerializer(many=True)

    class Meta:
        model = ToDoList
        fields = ('id', 'user', 'name', 'marker', 'items')

class CreateToDoListSerializer(serializers.ModelSerializer):

    class Meta:
        model = ToDoList
        fields = ('id', 'name', 'marker')


class ToDoListSerializerForMarkers(serializers.ModelSerializer):


    class Meta:
        model = ToDoList
        fields = ('id', 'name')


class MarkerSerializer(serializers.ModelSerializer):

    todo_lists = ToDoListSerializerForMarkers(many=True)

    class Meta:
        model = Marker
        fields = ('id', 'name', 'todo_lists')


class CreateMarkerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Marker
        fields = ('name',)
