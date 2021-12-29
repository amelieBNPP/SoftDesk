from rest_framework import routers
from backend.views import ProjectsViewset, ContributorsViewset, IssuesViewset, CommentViewSet
from django.urls import path, include

# Ici nous créons notre routeur
router = routers.SimpleRouter()
router.register('projects', ProjectsViewset, basename='projects')
router.register('contributors', ContributorsViewset, basename='contributors')
router.register('issues', IssuesViewset, basename='issues')
router.register('comment', CommentViewSet, basename='comment')


urlpatterns = [
    # Il faut bien penser à ajouter les urls du router dans la liste des urls disponibles.
    path('', include(router.urls)),
]
