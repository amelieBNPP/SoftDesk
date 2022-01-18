from rest_framework import routers
from rest_framework_nested import routers
from backend.views import (
    ProjectsViewset,
    ContributorsViewset,
    IssuesViewset,
    CommentViewSet,
)
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

issue_router = routers.NestedSimpleRouter(
    project_router,
    r'issues',
    lookup='issue',
)
issue_router.register(
    r'comments',
    CommentViewSet,
    basename='comments',
)

urlpatterns = [
    path('', include(router.urls)),
    path('', include(project_router.urls)),
    path('', include(issue_router.urls)),
]
