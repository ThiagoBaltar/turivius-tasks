import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    email = models.EmailField()

    def __str__(self):
        return self.email
