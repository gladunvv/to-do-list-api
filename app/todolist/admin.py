from django.contrib import admin
from todolist.models import List, Item, Marker


@admin.register(List)
class AdminList(admin.ModelAdmin):

    list_display = ('user', 'name')


@admin.register(Item)
class AdminItem(admin.ModelAdmin):

    list_display = ('title', 'priority', 'complited', 'created_date')
    list_filter = ('priority', 'complited', 'created_date')

@admin.register(Marker)
class AdminMarker(admin.ModelAdmin):

    list_display = ('name',)