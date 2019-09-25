from django.urls import path
from todolist.views import (
    ToDoListView,
    OneToDoListView,
)

app_name = 'todolist'

urlpatterns = [
    path('<int:pk>', OneToDoListView.as_view(), name='td_one'),
    path('all/', ToDoListView.as_view(), name='td_all'),
]