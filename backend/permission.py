from rest_framework.permissions import BasePermission, SAFE_METHODS
from .models import Contributors, Projects, Issues, Comment
from django.contrib.auth.models import User


class IsProjectAuthor(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        try:
            return obj.author == request.user
        except:
            author = Projects.objects.filter(
                pk=view.kwargs['project_pk']
            ).values()
            author_id = author[0]['author_id']
            author_user = User.objects.get(pk=author_id)
            return author_user == request.user


class IsProjectContributor(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            contributors = list(Contributors.objects.filter(
                project=view.kwargs['project_pk']
            ).values('user'))

            contributors_id = []
            for contributor in contributors:
                contributors_id.append(contributor['user'])
            return request.user.id in contributors_id
        return obj.author == request.user


class IsProjectManager(BasePermission):
    pass
