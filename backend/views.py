from backend.serializers import ProjectSerializer, ContributorsSerializer, IssuesSerializer, CommentSerializer
from backend.models import Projects, Contributors, Issues, Comment
from backend.permission import IsProjectAuthor, IsProjectContributor
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


class ProjectsViewset(ModelViewSet):
    '''
    This class allow to Create, Read, Update, Delete project. 
    Read and Update project are created by default thanks to ModelViewSet class.
    Create and Delete are overload below.
    '''
    # Nous récupérons tous les projets dans une variable nommée queryset
    queryset = Projects.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, IsProjectAuthor]

    def create(self, request):
        # Créer un projet et ajouter le contributeur à la liste de contributeur du projet
        request.data.update({'author': self.request.user.id})
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            new_contributor = Contributors(
                user=self.request.user,
                project=Projects.objects.last(),
                permission='author',
                role='author',
            )
            new_contributor.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.data, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        # Supprimer un projet, ses problèmes, ses contributeurs et ses commentaires
        project = get_object_or_404(Projects, pk=pk)
        self.check_object_permissions(request, project)
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
    permission_classes = [IsAuthenticated, IsProjectAuthor]

    def list(self, request, project_pk=None):
        project = get_object_or_404(Projects, pk=project_pk)
        self.check_object_permissions(request, project)
        queryset = Contributors.objects.filter(project=project_pk)
        serializer = ContributorsSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, project_pk=None):
        project = get_object_or_404(Projects, pk=project_pk)
        self.check_object_permissions(request, project)
        request.data.update({
            'project': str(project_pk),
            'permission': 'contributor',
        })
        serializer = ContributorsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None, project_pk=None):
        queryset = Contributors.objects.filter(pk=pk, project=project_pk)
        contributor = get_object_or_404(queryset, pk=pk)
        self.check_object_permissions(request, contributor)
        contributor.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class IssuesViewset(ModelViewSet):
    queryset = Issues.objects.all()
    serializer_class = IssuesSerializer
    permission_classes = [IsAuthenticated, IsProjectContributor]

    def list(self, request, project_pk=None):
        project = get_object_or_404(Projects, pk=project_pk)
        self.check_object_permissions(request, project)
        queryset = Issues.objects.filter(project=project_pk)
        serializer = IssuesSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, project_pk=None):
        project = get_object_or_404(Projects, pk=project_pk)
        self.check_object_permissions(request, project)
        request.data.update(
            {
                'project': project_pk,
                'author': self.request.user.id,
            }
        )
        serializer = IssuesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None, project_pk=None):
        queryset = Issues.objects.filter(pk=pk, project=project_pk)
        issue = get_object_or_404(queryset, pk=pk)
        self.check_object_permissions(request, issue)
        request.data.update(
            {
                'project': project_pk,
                'author': self.request.user.id,
            }
        )
        serializer = IssuesSerializer(issue, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None, project_pk=None):
        queryset = Issues.objects.filter(pk=pk, project=project_pk)
        issue = get_object_or_404(queryset, pk=pk)
        self.check_object_permissions(request, issue)
        issue.delete()
        comments = Comment.objects.filter(issue=pk)
        comments.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsProjectContributor]

    def list(self, request, project_pk=None, issue_pk=None):
        project = get_object_or_404(Projects, pk=project_pk)
        self.check_object_permissions(request, project)
        issues = Issues.objects.filter(project=project_pk)
        queryset = Comment.objects.filter(issue__in=issues)
        serializer = CommentSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, project_pk=None, issue_pk=None):
        issue = get_object_or_404(Issues, pk=issue_pk)
        self.check_object_permissions(request, issue)
        print(request.data)
        request.data.update(
            {
                'issue': issue_pk,
                'author': self.request.user.id,
            }
        )
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None, project_pk=None, issue_pk=None):
        queryset = Comment.objects.filter(pk=pk, issue=issue_pk)
        comment = get_object_or_404(queryset, pk=pk)
        self.check_object_permissions(request, comment)
        request.data.update(
            {
                'issue': issue_pk,
                'author': self.request.user.id,
            }
        )
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None, project_pk=None, issue_pk=None):
        queryset = Comment.objects.filter(pk=pk, issue=issue_pk)
        comment = get_object_or_404(queryset, pk=pk)
        self.check_object_permissions(request, comment)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
