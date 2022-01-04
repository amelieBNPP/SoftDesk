from django.db import models, transaction
from django.conf import settings
from django.db.models.enums import Choices

TAG = (
    ('bug', 'Bug'),
    ('feature', 'Feature'),
    ('improvement', 'Improvement'),
)

TYPE = (
    ('frontend', 'Frontend'),
    ('backend', 'Backend'),
    ('iOS', 'iOS'),
    ('android', 'Android'),
)

ROLE = (
    ('admin', 'Admin'),
    ('po', 'PO'),
    ('dev', 'Developer'),
)

PERMISSION = (
    ('author', 'Author'),
    ('contributor', 'Contributor'),
)

PRIORITY = (
    ('high', 'High'),
    ('medium', 'Medium'),
    ('low', 'Low'),
)

STATUS = (
    ('to do', 'To do'),
    ('in progress', 'In progress'),
    ('done', 'Done'),
)


class Projects(models.Model):
    title = models.CharField(max_length=128)
    description = models.CharField(max_length=2048, blank=True)
    type = models.CharField(choices=TYPE, max_length=128)
    author = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )


class Contributors(models.Model):
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    project = models.ForeignKey(
        to=Projects,
        on_delete=models.CASCADE,
    )
    permission = models.CharField(choices=PERMISSION, max_length=128)
    role = models.CharField(choices=ROLE, max_length=128)


class Issues(models.Model):
    title = models.CharField(max_length=128)
    desc = models.CharField(max_length=2048, blank=True)
    tag = models.CharField(choices=TAG, max_length=128)
    priority = models.CharField(choices=PRIORITY, max_length=128)
    project = models.ForeignKey(
        to=Projects,
        on_delete=models.CASCADE,
    )
    status = models.CharField(choices=STATUS, max_length=128)
    author = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='author_id',
    )
    assignee = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='assignee_id',
    )
    create_time = models.DateTimeField(auto_now=True)


class Comment(models.Model):
    description = models.CharField(max_length=2048, blank=True)
    author = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    issue = models.ForeignKey(
        to=Issues,
        on_delete=models.CASCADE,
    )
    create_time = models.DateTimeField(auto_now=True)
