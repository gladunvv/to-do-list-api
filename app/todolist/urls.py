from django.urls import path
from todolist.views import (
    UpdateItemView,
    CreateItemView,
    ToDoListView,
    OneToDoListView,
    CreateToDoListView,
    MarkerView,
    CreateMarker,
)

app_name = 'todolist'

urlpatterns = [
    path('<int:pk>/', OneToDoListView.as_view(), name='tdl_one'),
    path('all/', ToDoListView.as_view(), name='tdl_all'),
    path('create/', CreateToDoListView.as_view(), name='tdl_create'),
    path('<int:pk>/create/', CreateItemView.as_view(), name='item_create'),
    path('<int:tdl_pk>/<int:it_pk>/update/', UpdateItemView.as_view(), name='item_update'),
    path('marker/all/', MarkerView.as_view(), name='mk_all'),
    path('marker/create/', CreateMarker.as_view(), name='mk_create'),
]
