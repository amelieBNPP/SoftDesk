from rest_framework import routers
from rest_framework_nested import routers
from backend.views import ProjectsViewset, ContributorsViewset, IssuesViewset, CommentViewSet
from django.urls import path, include

# Ici nous créons notre routeur
router = routers.SimpleRouter()
router.register('projects', ProjectsViewset, basename='projects')
router.register('contributors', ContributorsViewset, basename='contributors')
router.register('issues', IssuesViewset, basename='issues')
router.register('comment', CommentViewSet, basename='comment')

project_router = routers.NestedSimpleRouter(
    router,
    r'projects',
    lookup='project',
)
project_router.register(r'issues', IssuesViewset, basename='issues')
project_router.register(
    r'users',
    ContributorsViewset,
    basename='users',
)

urlpatterns = [
    # Il faut bien penser à ajouter les urls du router dans la liste des urls disponibles.
    path('', include(router.urls)),
    path('', include(project_router.urls)),
]
