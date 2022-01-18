import json
from backend.models import Projects, Issues, Comment, Contributors
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.test import Client, TestCase
from rest_framework import status


class ProjectAPITestCase(TestCase):

    def setUp(self) -> None:

        self.client_durant_info = {
            'username': 'durant',
            'email': 'durant@test.com',
            'password': 'MyPassword00',
        }

        self.client_dupont_info = {
            'username': 'dupont',
            'email': 'dupont@test.com',
            'password': 'MySecret00',
        }

        self._create_user(self.client_durant_info)
        self._create_user(self.client_dupont_info)

        self.client_durant = self._get_client(self.client_durant_info)
        self.client_dupont = self._get_client(self.client_dupont_info)

    def test_post_project(self) -> None:
        """ Test add project """
        request = {
            'title': 'title1',
            'description': 'description1',
            'type': 'backend',
        }
        response = self.client_durant.post(
            '/api/projects/',
            request,
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        request_id = json.loads(response.content)['id']
        request_db = Projects.objects.filter(pk=request_id).values()
        self.assertEqual(request_db[0]['title'], request['title'])
        self.assertEqual(request_db[0]['description'], request['description'])
        self.assertEqual(request_db[0]['type'], request['type'])

    def test_get_projects(self) -> None:
        """ Test get all projects """
        response = self.client_durant.get('/api/projects/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_project(self) -> None:
        """ Test delete a project """
        request = {
            'title': 'title1',
            'description': 'description1',
            'type': 'backend',
        }
        project_id = self._create_project(self.client_durant, request)['id']

        response = self.client_durant.delete(f'/api/projects/{project_id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        project_exist = Projects.objects.filter(pk=project_id).exists()
        self.assertEqual(project_exist, False)

    def test_delete_project_without_permission(self) -> None:
        """ Test delete project from a non contributor to the project """
        request = {
            'title': 'title1',
            'description': 'description1',
            'type': 'backend',
        }
        project_id = self._create_project(self.client_durant, request)['id']

        response = self.client_dupont.delete(f'/api/projects/{project_id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        project_exist = Projects.objects.filter(pk=project_id).exists()
        self.assertEqual(project_exist, True)

    def _get_client(self, client_info):
        """ Create client with token """
        response = self.client.post(
            '/user/login/',
            {
                'username': client_info['username'],
                'password': client_info['password'],
            },
        )
        response_data = json.loads(response.content)
        return Client(
            HTTP_AUTHORIZATION='Bearer ' + response_data['token']
        )

    @staticmethod
    def _create_user(client_info):
        """ Create user """
        return User.objects.create(
            username=client_info['username'],
            password=make_password(client_info['password']),
        )

    @staticmethod
    def _create_project(client, project) -> None:
        """ Create project """
        response = client.post(
            '/api/projects/',
            project,
        )
        return json.loads(response.content)
