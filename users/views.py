import re
from django.shortcuts import render
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.settings import api_settings
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.signals import user_logged_in
from users.serializers import UserSerializer
import jwt
import datetime
from SoftDesk.settings import JWT_AUTH
# super user amelienoury PW4admin
# https://www.youtube.com/watch?v=PUzgZrS_piQ


class CreateUserView(APIView):
    # Allow any user (authenticated or not) to access this url
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginUserView(APIView):
    def post(self, request):
        username = request.data['username']
        password = request.data['password']

        user = User.objects.filter(username=username).first()

        if user is None:
            raise AuthenticationFailed('User not found!')

        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password!')

        payload = {
            'id': user.id,
            'username': user.username,
            'exp': datetime.datetime.utcnow() + JWT_AUTH['JWT_EXPIRATION_DELTA'],
            'iat': datetime.datetime.utcnow(),
        }

        token = jwt.encode(
            payload,
            JWT_AUTH['JWT_SECRET_KEY'],
            algorithm=JWT_AUTH['JWT_ALGORITHM']
        ).decode('utf-8')

        response = Response()
        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'token': token,
        }
        return response


class UserView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')
        try:
            payload = jwt.decode(
                token,
                JWT_AUTH['JWT_SECRET_KEY'],
                algorithms=JWT_AUTH['JWT_ALGORITHM'],
            )
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        user = User.objects.filter(id=payload['id']).first()
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request):
        pass


class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'success'
        }
        return response
