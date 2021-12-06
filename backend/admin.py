from django.contrib import admin

from .models import Projects, Comment, Contributors, Issues

admin.site.register(Projects)
admin.site.register(Comment)
admin.site.register(Contributors)
admin.site.register(Issues)
