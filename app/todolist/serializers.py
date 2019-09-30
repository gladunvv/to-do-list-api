from rest_framework import serializers
from todolist.models import ToDoList, Item, Marker


class ItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = Item
        fields = ('title', 'priority', 'complited', 'notification_date', 'created_date')


class ToDoListSerializer(serializers.ModelSerializer):

    items = ItemSerializer(many=True)

    class Meta:
        model = ToDoList
        fields = ('user', 'name', 'marker', 'items')

class CreateToDoListSerializer(serializers.ModelSerializer):

    class Meta:
        model = ToDoList
        fields = ('name', 'marker')


class ToDoListSerializerForMarkers(serializers.ModelSerializer):

    items = ItemSerializer(many=True)

    class Meta:
        model = ToDoList
        fields = ('name', 'items',)

class MarkerSerializer(serializers.ModelSerializer):

    todo_lists = ToDoListSerializerForMarkers(many=True)

    class Meta:
        model = Marker
        fields = ('name', 'todo_lists', )
