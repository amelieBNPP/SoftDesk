from django.db import models
from django.conf import settings


class Projects(models.Model):
    title = models.CharField(max_length=128)
    description = models.IntegerField(default=0)
    type = models.CharField(max_length=128)
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
    permission = models.CharField(max_length=128)
    role = models.CharField(max_length=128)


class Issues(models.Model):
    title = models.CharField(max_length=128)
    desc = models.CharField(max_length=2048, blank=True)
    tag = models.CharField(max_length=128)
    priority = models.CharField(max_length=128)
    project = models.ForeignKey(
        to=Projects,
        on_delete=models.CASCADE,
    )
    status = models.CharField(max_length=128)
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
