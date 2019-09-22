from django.urls import path
from user.views import UserAuthToken

app_name = 'user'

urlpatterns = [
    path('create/', UserAuthToken.as_view(), name='user_create'),
]