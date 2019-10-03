from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken

from user.messages import send_verification_email
from user.serializers import CreateUserSerializer


class UserAuthToken(APIView):

    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = CreateUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            if user:
                token = Token.objects.create(user=user)
                json = serializer.data
                json['token'] = token.key

            send_verification_email(request, user, token)
            return Response(json, status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class UserLogIn(ObtainAuthToken):

    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })


class UserVerificationEmail(APIView):

    permission_classes = (permissions.AllowAny,)

    def get(self, request, *args, **kwargs):
        uid = request.GET.get('uid', None)
        token = request.GET.get('token', None)

        if not uid or not token:
            return Response({'errors': ['No uid or token provided']}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user_id = urlsafe_base64_decode(uid)
            user = User.objects.get(pk=user_id)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        token = Token.objects.get(user=user)
        if user and token:
            message = {
                'message': 'Congratulations dear {} you have successfully registered!'.format(
                    user.username
                ),
                'token': token.key,
            }
            return Response(message, status=status.HTTP_200_OK)

        return Response({'errors': ['Invalid user or token']}, status=status.HTTP_400_BAD_REQUEST)


class UserDelete(APIView):

    permission_classes = (permissions.IsAuthenticated,)

    def delete(self, request, *args, **kwargs):
        user = request.user
        request.user.delete()
        message = {
            'message': 'User {user} deleted successfully'.format(
                user=user.username,
            ),
        }
        return Response(message, status=status.HTTP_200_OK)


class UserLogOut(APIView):

    permission_classes = (permissions.IsAuthenticated, )

    def post(self, request, format=None):
        request.user.auth_token.delete()
        msg = ('You have successfully logged out the application')
        return Response({'message': msg}, status=status.HTTP_200_OK)
