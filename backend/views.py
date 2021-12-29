from rest_framework.views import APIView
from backend.serializers import ProjectSerializer, ContributorsSerializer, IssuesSerializer, CommentSerializer
from backend.models import STATUS, Projects, Contributors, Issues, Comment
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated


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
            'author': self.request.user.id,
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
        project = get_object_or_404(Projects, pk=pk)
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
