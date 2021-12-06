from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer

from backend.models import Contributors, Projects


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class ProjectSerializer(ModelSerializer):
    class Meta:
        model = Projects
        fields = ['title', 'description', 'type', 'author']


class ContributorsSerializer(ModelSerializer):
    class Meta:
        model = Contributors
        fields = ['user', 'project', 'permission', 'role']


class IssuesSerializer(ModelSerializer):
    class Meta:
        model = Contributors
        fields = [
            'title',
            'desc',
            'tag',
            'priority',
            'project',
            'status',
            'author',
            'assignee',
            'create_time',
        ]
