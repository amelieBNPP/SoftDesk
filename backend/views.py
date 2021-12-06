from rest_framework.viewsets import ReadOnlyModelViewSet

from backend.models import Projects, Contributors, Issues, Comment
from backend.serializers import ProjectSerializer, ContributorsSerializer, IssuesSerializer


class ProjectsViewset(ReadOnlyModelViewSet):

    serializer_class = ProjectSerializer

    def get_queryset(self):
        # Nous récupérons tous les projets dans une variable nommée queryset
        queryset = Projects.objects.all()

        # Vérifions la présence du paramètre ‘project_id’ dans l’url et si oui alors appliquons notre filtre
        project_id = self.request.GET.get('project_id')
        if project_id is not None:
            queryset = queryset.filter(project_id=project_id)
        return queryset


class ContributorsViewset(ReadOnlyModelViewSet):

    serializer_class = ContributorsSerializer

    def get_queryset(self):
        # Nous récupérons tous les projets dans une variable nommée queryset
        queryset = Contributors.objects.all()

        # Vérifions la présence du paramètre ‘project_id’ dans l’url et si oui alors appliquons notre filtre
        contributor_id = self.request.GET.get('contributor_id')
        if contributor_id is not None:
            queryset = queryset.filter(contributor_id=contributor_id)
        return queryset


class IssuesViewset(ReadOnlyModelViewSet):

    serializer_class = IssuesSerializer

    def get_queryset(self):
        # Nous récupérons tous les projets dans une variable nommée queryset
        queryset = Issues.objects.all()

        # Vérifions la présence du paramètre ‘project_id’ dans l’url et si oui alors appliquons notre filtre
        issue_id = self.request.GET.get('issue_id')
        if issue_id is not None:
            queryset = queryset.filter(issue_id=issue_id)
        return queryset
