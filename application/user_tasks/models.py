import uuid

from django.db import models

from users.models import User


class UserTask(models.Model):
    user = models.ForeignKey(User, models.CASCADE, related_name='tasks')
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, default='')
    finished = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
