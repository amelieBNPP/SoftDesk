from backend.serializers import (
    ProjectSerializer,
    ContributorsSerializer,
    IssuesSerializer,
    CommentSerializer,
)
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
    Read and Update project are created by default
    thanks to ModelViewSet class.
    Create and Delete are overload below.
    '''
    # Nous récupérons tous les projets dans une variable nommée queryset
    queryset = Projects.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, IsProjectAuthor]

    def create(self, request):
        """
        Create project and add contributor to contributor's project list.
        """
        request_data = request.data.copy()
        request_data.update({'author': self.request.user.id})
        serializer = ProjectSerializer(data=request_data)
        if serializer.is_valid():
            serializer.save()
            new_contributor = Contributors(
                user=self.request.user,
                project=Projects.objects.last(),
                permission='author',
                role='author',
            )
            new_contributor.save()
            return Response(
                data=serializer.data,
                status=status.HTTP_201_CREATED,
            )
        return Response(
            data=serializer.data,
            status=status.HTTP_400_BAD_REQUEST,
        )

    def destroy(self, request, pk=None):
        """
        Delete a project, its issues, its contributors and comments.
        """
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
        """ GET all projects if permission"""
        project = get_object_or_404(Projects, pk=project_pk)
        self.check_object_permissions(request, project)
        queryset = Contributors.objects.filter(project=project_pk)
        serializer = ContributorsSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, project_pk=None):
        """Create project if permission and add the owner as contributor."""
        project = get_object_or_404(Projects, pk=project_pk)
        self.check_object_permissions(request, project)
        request_data = request.data.copy()
        request_data.update({
            'project': str(project_pk),
            'permission': 'contributor',
        })
        serializer = ContributorsSerializer(data=request_data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None, project_pk=None):
        """Delete project if permission and if object exist."""
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
        """ Get all issues for a specific project if permission. """
        project = get_object_or_404(Projects, pk=project_pk)
        self.check_object_permissions(request, project)
        queryset = Issues.objects.filter(project=project_pk)
        if len(queryset) == 0:
            return Response("no issue for this project")
        serializer = IssuesSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None, project_pk=None):
        """
        Get a specific issue for a specific project
        if object exist and if permission.
        """
        issue = get_object_or_404(Issues, pk=pk, project=project_pk)
        self.check_object_permissions(request, issue)
        queryset = Issues.objects.filter(pk=pk)
        serializer = IssuesSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, project_pk=None):
        """ create issue if project exist and if permission"""
        project = get_object_or_404(Projects, pk=project_pk)
        self.check_object_permissions(request, project)
        request_data = request.data.copy()
        request_data.update(
            {
                'project': project_pk,
                'author': self.request.user.id,
            }
        )
        serializer = IssuesSerializer(data=request_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None, project_pk=None):
        """
        Update an issue if issue and project exists
        and if permission
        """
        queryset = Issues.objects.filter(pk=pk, project=project_pk)
        issue = get_object_or_404(queryset, pk=pk)
        self.check_object_permissions(request, issue)
        request_data = request.data.copy()
        request_data.update(
            {
                'project': project_pk,
                'author': self.request.user.id,
            }
        )
        serializer = IssuesSerializer(issue, data=request_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None, project_pk=None):
        """Delete issue if project and issue exists and if permission"""
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
        """
        Get all comment for a specific project-issue
        if project-issue exists
        if permission.
        """
        project = get_object_or_404(Projects, pk=project_pk)
        self.check_object_permissions(request, project)
        issues = get_object_or_404(Issues, pk=issue_pk, project=project_pk)
        queryset = Comment.objects.filter(issue=issues.id)
        if len(queryset) == 0:
            return Response("no comment for this project / issue")
        serializer = CommentSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, project_pk=None, issue_pk=None, pk=None):
        """
        Get a specific comment for a specific project-issue
        if project-issue-comment exists
        if permission.
        """
        project = get_object_or_404(Projects, pk=project_pk)
        self.check_object_permissions(request, project)
        comment = get_object_or_404(Comment, issue=issue_pk, pk=pk)
        issues = Issues.objects.filter(project=project_pk)
        get_object_or_404(issues, pk=comment.issue.id)
        queryset = Comment.objects.filter(issue__in=issues, pk=pk)
        serializer = CommentSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, project_pk=None, issue_pk=None):
        """
        Create a comment for specific project-issue
        if permission
        """
        issue = get_object_or_404(Issues, pk=issue_pk)
        self.check_object_permissions(request, issue)
        request_data = request.data.copy()
        request_data.update(
            {
                'issue': issue_pk,
                'author': self.request.user.id,
            }
        )
        serializer = CommentSerializer(data=request_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None, project_pk=None, issue_pk=None):
        """
        Update a comment for specific project-issue-comment
        if the project-issue-comment exist and
        if permission
        """
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
        """
        Delete a specific project-issue-comment if object exist
        if permission.
        """
        queryset = Comment.objects.filter(pk=pk, issue=issue_pk)
        comment = get_object_or_404(queryset, pk=pk)
        self.check_object_permissions(request, comment)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
