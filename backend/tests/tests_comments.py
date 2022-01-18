from http import client
import json
from backend.models import Projects, Issues, Comment, Contributors
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.test import Client, TestCase
from rest_framework import status


class CommentsAPITestCase(TestCase):

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

        self.issue1_info = {
            'title': 'issue1',
            'desc': 'manage issue 1',
            'tag': 'bug',
            'priority': 'medium',
            'status': 'contributor',
        }
        self.issue1 = self._create_issue(
            self.issue1_info,
            self.project1,
            self.user_dupont,
            self.user_durant,
        )

        self.issue2_info = {
            'title': 'issue2',
            'desc': 'manage issue 2',
            'tag': 'feature',
            'priority': 'low',
            'status': 'contributor',
        }
        self.issue2 = self._create_issue(
            self.issue2_info,
            self.project1,
            self.user_durant,
            self.user_dupont,
        )

    def test_get_issue_comments(self) -> None:
        comment = Comment.objects.create(
            description='comment 1 of issue 1',
            author=self.user_dupont,
            issue=self.issue1,
        )
        response = self.client_durant.get(
            ('/api/projects/' + str(self.project1.id) +
             '/issues/' + str(self.issue1.id) + '/comments/'),
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(json.loads(response.content)), 0)

    def test_post_issue_comments(self) -> None:
        request = {
            'description': 'comment 1 of issue 1',
        }
        response = self.client_dupont.post(
            ('/api/projects/' + str(self.project1.id) +
             '/issues/' + str(self.issue1.id) + '/comments/'),
            request
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_issue_comments(self) -> None:
        comment = Comment.objects.create(
            description='comment 1 of issue 1',
            author=self.user_dupont,
            issue=self.issue1,
        )

        request = {
            'description': 'update comment 1 of issue 1',
        }
        response = self.client_dupont.put(
            ('/api/projects/' + str(self.project1.id) +
             '/issues/' + str(self.issue1.id) +
             '/comments/' + str(comment.id) + '/'),
            request,
            content_type='application/json',
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            json.loads(response.content)['description'],
            request['description'])

    def test_delete_issue_comment(self) -> None:
        comment = Comment.objects.create(
            description='comment 1 of issue 1',
            author=self.user_dupont,
            issue=self.issue1,
        )
        response = self.client_dupont.delete(
            ('/api/projects/' + str(self.project1.id) +
             '/issues/' + str(self.issue1.id) +
             '/comments/' + str(comment.id) + '/'),
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(Comment.objects.filter(pk=comment.id)), 0)

    def test_delete_issue_comment_without_permission(self) -> None:
        comment = Comment.objects.create(
            description='comment 1 of issue 1',
            author=self.user_dupont,
            issue=self.issue1,
        )
        response = self.client_durant.delete(
            ('/api/projects/' + str(self.project1.id) +
             '/issues/' + str(self.issue1.id) +
             '/comments/' + str(comment.id) + '/'),
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(len(Comment.objects.filter(pk=comment.id)), 1)

    def _get_client(self, client_info):
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
        return User.objects.create(
            username=client_info['username'],
            password=make_password(client_info['password']),
        )

    @ staticmethod
    def _create_project(project_info, author) -> None:
        return Projects.objects.create(
            title=project_info['title'],
            description=project_info['description'],
            type=project_info['type'],
            author=author,
        )

    @staticmethod
    def _create_contributor(contributor_info) -> Contributors:
        return Contributors.objects.create(
            user=contributor_info['user'],
            project=contributor_info['project'],
            role=contributor_info['role'],
            permission=contributor_info['permission'],
        )

    @staticmethod
    def _create_issue(issue_info, project, author, assignee) -> Issues:
        return Issues.objects.create(
            project=project,
            title=issue_info['title'],
            desc=issue_info['desc'],
            tag=issue_info['tag'],
            priority=issue_info['priority'],
            status=issue_info['status'],
            author=author,
            assignee=assignee,
        )
