import json
from rest_framework import status
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.test import Client, TestCase


class AuthentificationAPITestCase(TestCase):

    def setUp(self) -> None:
        self.client = Client()

        self.client_info = {
            'username': 'durant',
            'email': 'durant@test.com',
            'password': 'MyPassword00',
        }

        User.objects.create(
            username=self.client_info['username'],
            password=make_password(self.client_info['password']),
        )

        self.token = self._get_token(
            self.client_info['username'],
            self.client_info['password'],
        )
        self.client_durant = Client(
            HTTP_AUTHORIZATION='Bearer ' + self.token['token']
        )

    def _get_token(self, user, password):
        response = self.client.post(
            '/user/login/',
            {
                'username': user,
                'password': password,
            },
        )
        return json.loads(response.content)

    def test_create_user(self) -> None:
        client_info = {
            'username': 'dupont',
            'email': 'dupont@test.com',
            'password': 'MySecret00',
        }
        response = self.client.post('/user/signup/', client_info)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response_json = json.loads(response.content)
        self.assertEqual(response_json['username'], client_info['username'])
        self.assertEqual(response_json['email'], client_info['email'])

    def test_login_user(self) -> None:
        client_data = {
            'username': self.client_info['username'],
            'password': self.client_info['password'],
        }
        response = self.client.post('/user/login/', client_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
