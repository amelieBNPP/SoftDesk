from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from backend.models import Comment, Contributors, Projects, Issues


class ProjectSerializer(ModelSerializer):
    class Meta:
        model = Projects
        fields = ['id', 'title', 'description', 'type', 'author']

    def validate_project(self, value):
        if Projects.objects.filter(title=value).exists():
            raise serializers.ValidationError('Project already exists')
        return value


class ContributorsSerializer(ModelSerializer):
    class Meta:
        model = Contributors
        fields = ['user', 'project', 'permission', 'role']


class IssuesSerializer(ModelSerializer):
    class Meta:
        model = Issues
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


class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            'description',
            'author',
            'issue',
            'create_time',
        ]
