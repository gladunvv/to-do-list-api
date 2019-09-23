from django.urls import path
from user.views import UserAuthToken, UserLogin, UserVerificationEmail

app_name = 'user'

urlpatterns = [
    path('create/', UserAuthToken.as_view(), name='createuser'),
    path('login/', UserLogin.as_view(), name='login'),
    path('verification/', UserVerificationEmail.as_view(), name='verification'),
]