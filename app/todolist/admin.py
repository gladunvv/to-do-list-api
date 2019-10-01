from django.contrib import admin
from todolist.models import ToDoList, Item, Marker


@admin.register(ToDoList)
class AdminToDoList(admin.ModelAdmin):

    list_display = ('name', 'user')


@admin.register(Item)
class AdminItem(admin.ModelAdmin):

    list_display = ('title', 'priority', 'complited', 'created_date')
    list_filter = ('priority', 'complited', 'created_date')


@admin.register(Marker)
class AdminMarker(admin.ModelAdmin):

    list_display = ('name',)