from django.urls import path
from user.views import (
    UserAuthToken,
    UserLogIn,
    UserVerificationEmail,
    UserLogOut,
    UserDelete,
    )

app_name = 'user'

urlpatterns = [
    path('create/', UserAuthToken.as_view(), name='createuser'),
    path('login/', UserLogIn.as_view(), name='login'),
    path('verification/', UserVerificationEmail.as_view(), name='verification'),
    path('logout/', UserLogOut.as_view(), name='logout'),
    path('delete/', UserDelete.as_view(), name='delete'),
]