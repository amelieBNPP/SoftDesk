from django.contrib.auth.models import User, Group
from rest_framework.serializers import ModelSerializer

from backend.models import Projects


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(ModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class ProjectSerializer(ModelSerializer):
    class Meta:
        model = Projects
        fields = ['title', 'description', 'type', 'author']
