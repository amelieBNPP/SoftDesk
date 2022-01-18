import json
from backend.models import Projects, Issues, Comment, Contributors
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.test import Client, TestCase
from rest_framework import status


class IssuesAPITestCase(TestCase):

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

        self.project1_info = {
            'title': 'title1',
            'description': 'description1',
            'type': 'backend',
        }
        self.project1 = self._create_project(
            self.project1_info,
            self.user_durant,
        )
        self.project2_info = {
            'title': 'title2',
            'description': 'description2',
            'type': 'frontend',
        }
        self.project2 = self._create_project(
            self.project2_info,
            self.user_dupont,
        )

        self.contributor1_info = {
            'user': self.user_durant,
            'project': self.project1,
            'permission': 'contributor',
            'role': 'dev',
        }
        self.contributor1 = self._create_contributor(
            self.contributor1_info,
        )

        self.contributor2_info = {
            'user': self.user_dupont,
            'project': self.project2,
            'permission': 'contributor',
            'role': 'po',
        }
        self.contributor2 = self._create_contributor(
            self.contributor2_info,
        )

    def test_get_project_issues(self) -> None:
        """ Get all issue of a project """
        Issues.objects.create(
            project=self.project1,
            title='issue to manage',
            desc='test ajout issue ',
            tag='bug',
            priority='medium',
            status='in progress',
            author=self.user_durant,
            assignee=self.user_dupont,
        )
        response = self.client_durant.get(
            f'/api/projects/{self.project1.id}/issues/',
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(json.loads(response.content)), 0)

    def test_post_project_issue(self) -> None:
        """ Add an issue to a specific project """
        request = {
            'title': 'issue to manage',
            'desc': 'test ajout issue ',
            'tag': 'bug',
            'priority': 'low',
            'status': 'to do',
            'assignee': self.user_dupont,
        }
        response = self.client_durant.post(
            f'/api/projects/{self.project1.id}/issues/',
            request
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_delete_project_issue(self) -> None:
        """ Delete an issue from specific project """
        issue_id = Issues.objects.create(
            project=self.project1,
            title='issue to manage',
            desc='test ajout issue ',
            tag='bug',
            priority='medium',
            status='in progress',
            author=self.user_durant,
            assignee=self.user_dupont,
        ).id

        response = self.client_durant.delete(
            f'/api/projects/{self.project1.id}/issues/{issue_id}/'
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(Issues.objects.filter(pk=issue_id)), 0)

    def test_delete_project_issue_without_permission(self) -> None:
        """ Test delete issue from a non contributor to the project """
        issue_id = Issues.objects.create(
            project=self.project1,
            title='issue to manage',
            desc='test ajout issue ',
            tag='bug',
            priority='medium',
            status='in progress',
            author=self.user_durant,
            assignee=self.user_dupont,
        ).id

        response = self.client_dupont.delete(
            f'/api/projects/{self.project1.id}/issues/{issue_id}/'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(len(Issues.objects.filter(pk=issue_id)), 1)

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
    def _create_project(project_info, author) -> None:
        """ Create project """
        return Projects.objects.create(
            title=project_info['title'],
            description=project_info['description'],
            type=project_info['type'],
            author=author,
        )

    @staticmethod
    def _create_contributor(contributor_info) -> Contributors:
        """ Create contributor """
        return Contributors.objects.create(
            user=contributor_info['user'],
            project=contributor_info['project'],
            role=contributor_info['role'],
            permission=contributor_info['permission'],
        )
