from django.urls import path
from todolist.views import (
    UpdateItemView,
    CreateItemView,
    ToDoListView,
    OneToDoListView,
    CreateToDoListView,
    MarkerView
)

app_name = 'todolist'

urlpatterns = [
    path('<int:pk>', OneToDoListView.as_view(), name='td_one'),
    path('<int:pk>/create/', CreateItemView.as_view(), name='item_create'),
    path('<int:td_pk>/<int:it_pk>/update/', UpdateItemView.as_view(), name='item_update'),
    path('all/', ToDoListView.as_view(), name='td_all'),
    path('create/', CreateToDoListView.as_view(), name='td_create'),
    path('marker/all/', MarkerView.as_view(), name='mk_all')
]