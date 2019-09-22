from rest_framework import status
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken

from user.serializers import CreateUserSerializer

class UserAuthToken(APIView):

    permission_classes = (permissions.AllowAny,)

    def post(self, request, format='json'):
        serializer = CreateUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            if user:
                token = Token.objects.create(user=user)
                response = serializer.data
                response['token'] = token.key

            return Response(response, status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

