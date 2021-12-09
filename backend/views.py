from rest_framework import serializers, status
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet, ViewSet
from rest_framework.response import Response
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated, BasePermission
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import Permission, User
from backend.models import STATUS, Projects, Contributors, Issues, Comment
from backend.serializers import ProjectSerializer, ContributorsSerializer, IssuesSerializer, CommentSerializer


class IsOwnerOrReadOnly(BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the snippet.
        return obj.owner == request.user


class ProjectsViewset(ModelViewSet):
    '''
    This class allow to Create, Read, Update, Delete project. 
    Read and Update project are created by default thanks to ModelViewSet class.
    Create and Delete are overload below.
    '''
    # Nous récupérons tous les projets dans une variable nommée queryset
    queryset = Projects.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request):
        # Créer un projet et ajouter le contributeur à la liste de contributeur du projet
        post_project = {
            'title': request.data['title'],
            'description': request.data['description'],
            'type': request.data['type'],
            'author': request.data['author'],
        }
        serializer = ProjectSerializer(data=post_project)
        if serializer.is_valid():
            serializer.save()
            new_contributor = Contributors(
                user=self.request.user,
                project=Projects.objects.last(),
                permission='admin',
                role='admin',
            )
            new_contributor.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.data, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        # Supprimer un projet, ses problèmes, ses contributeurs et ses commentaires
        project = get_object_or_404(self.queryset, pk=pk)
        project.delete()
        contributors = Contributors.objects.filter(project=pk)
        contributors.delete()
        issues = Issues.objects.filter(project=pk)
        for issue in issues:
            comments = Comment.objects.filter(issue=issue)
            comments.delete()
        issues.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ContributorsViewset(ModelViewSet):
    queryset = Contributors.objects.all()
    serializer_class = ContributorsSerializer

    # def list(self, request, project_pk=None):
    #     pass

    # def create(self, request, project_pk=None):
    #     pass

    # def destroy(self, request, pk=None, project_pk=None):
    #     pass


class IssuesViewset(ModelViewSet):
    queryset = Issues.objects.all()
    serializer_class = IssuesSerializer

    # def list(self, request, project_pk=None):
    #     pass

    # def retrieve(self, request, pk=None, project_pk=None):
    #     pass

    # def create(self, request, project_pk=None):
    #     pass

    # def update(self, request, pk=None, project_pk=None):
    #     pass

    # def destroy(self, request, pk=None, project_pk=None):
    #     pass


class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    # def list(self, request, project_pk=None, issue_pk=None):
    #     pass

    # def retrieve(self, request, pk=None, project_pk=None, issue_pk=None):
    #     pass

    # def create(self, request, project_pk=None, issue_pk=None):
    #     pass

    # def update(self, request, pk=None, project_pk=None, issue_pk=None):
    #     pass

    # def destroy(self, request, pk=None, project_pk=None, issue_pk=None):
    #     pass
