from django.urls import reverse_lazy
from rest_framework.test import APITestCase

from backend.models import Projects, Issues, Comment, Contributors
from django.contrib.auth.models import User
from django.test import Client


class backendAPITestCase(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = User.objects.create_user(
            username='admin',
            email='admin@test.com',
            password='my_secret',
        )


class TestProject(backendAPITestCase):
    # Nous stockons l’url de l'endpoint dans un attribut de classe pour pouvoir l’utiliser plus facilement dans chacun de nos tests
    url = reverse_lazy('projects-list')

    def test_list(self):
        # Créons un projet
        project = Projects.objects.create(
            title='ProjetTest',
            author=self.user,
        )
        # On réalise l’appel en GET en utilisant le client de la classe de test
        response = self.client.get(self.url)
        # Nous vérifions que le status code est bien 200
        # et que les valeurs retournées sont bien celles attendues
        self.assertEqual(response.status_code, 200)
        excepted = [
            {
                'title': project.title,
                'description': project.description,
                'type': project.type,
                'author': project.author.pk,
            }
        ]
        self.assertEqual(excepted, response.json())
