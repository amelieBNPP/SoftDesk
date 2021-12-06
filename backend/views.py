from rest_framework.viewsets import ModelViewSet

from backend.models import Projects, Contributors, Issues, Comment
from backend.serializers import ProjectSerializer


class ProjectsViewset(ModelViewSet):

    serializer_class = ProjectSerializer

    def get_queryset(self):
        return Projects.objects.all()
