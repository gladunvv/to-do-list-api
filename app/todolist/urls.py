from django.urls import path
from todolist.views import ToDoListView

app_name = 'todolist'

urlpatterns = [
    path('all/', ToDoListView.as_view(), name='td_all')
]