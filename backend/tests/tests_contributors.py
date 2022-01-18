import json
from backend.models import Projects, Issues, Comment, Contributors
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.test import Client, TestCase
from rest_framework import status


class ContributorsAPITestCase(TestCase):

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

        self.user_durant = self._create_user(self.client_durant_info)
        self.user_dupont = self._create_user(self.client_dupont_info)

        self.client_durant = self._get_client(self.client_durant_info)
        self.client_dupont = self._get_client(self.client_dupont_info)

    def test_get_project_contributor(self) -> None:
        """ Get all project contributor"""
        request = {
            'title': 'title1',
            'description': 'description1',
            'type': 'backend',
        }
        project = self._create_project(self.client_durant, request)
        project_id = project['id']
        project_author = project['author']

        response = self.client_durant.get(
            f'/api/projects/{project_id}/users/',
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        contributors = json.loads(response.content)
        contributors_id = [contributor['id'] for contributor in contributors]
        self.assertIn(project_author, contributors_id)

    def test_post_project_contributor(self) -> None:
        """ Add a contributor to a specific project """
        request = {
            'title': 'title1',
            'description': 'description1',
            'type': 'backend',
        }
        project_id = self._create_project(self.client_durant, request)['id']
        contributors_init = len(
            Contributors.objects.filter(project_id=project_id)
        )

        request = {
            'user': self.client_dupont_info['username'],
            'role': 'dev',
        }
        response = self.client_durant.post(
            f'/api/projects/{project_id}/users/',
            request
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        contributors_final = len(
            Contributors.objects.filter(project_id=project_id)
        )

        self.assertEqual(contributors_init+1, contributors_final)

    def test_delete_project_contributor(self) -> None:
        """ Delete contributor from specific project """
        request = {
            'title': 'title1',
            'description': 'description1',
            'type': 'backend',
        }
        project_id = self._create_project(self.client_durant, request)['id']
        project = Projects.objects.get(pk=project_id)

        contributor = Contributors.objects.create(
            user=self.user_dupont,
            project=project,
            permission='contributor',
            role='dev'
        )
        contributors_init = len(
            Contributors.objects.filter(project_id=project_id)
        )
        response = self.client_durant.delete(
            f'/api/projects/{project_id}/users/{contributor.id}/'
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        contributors_final = len(
            Contributors.objects.filter(project_id=project_id)
        )
        self.assertEqual(contributors_init, contributors_final+1)

    def test_delete_project_contributor_without_permission(self) -> None:
        """ Test delete contributor from a non contributor to the project """
        request = {
            'title': 'title1',
            'description': 'description1',
            'type': 'backend',
        }
        project_id = self._create_project(self.client_durant, request)['id']
        project = Projects.objects.get(pk=project_id)

        contributor = Contributors.objects.create(
            user=self.user_dupont,
            project=project,
            permission='contributor',
            role='dev'
        )
        contributors_init = len(
            Contributors.objects.filter(project_id=project_id)
        )
        response = self.client_dupont.delete(
            f'/api/projects/{project_id}/users/{contributor.id}/'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        contributors_final = len(
            Contributors.objects.filter(project_id=project_id)
        )
        self.assertEqual(contributors_init, contributors_final)

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

    @ staticmethod
    def _create_user(client_info):
        """ Create user """
        return User.objects.create(
            username=client_info['username'],
            password=make_password(client_info['password']),
        )

    @ staticmethod
    def _create_project(client, project) -> None:
        """ Create project """
        response = client.post(
            '/api/projects/',
            project,
        )
        return json.loads(response.content)

    @staticmethod
    def _create_contributor(client, project_id, contributor) -> None:
        """ Create contributor """
        request = {
            'user': contributor['username'],
            'role': 'dev',
        }
        response = client.post(
            f'/api/projects/{project_id}/users/',
            request
        )
