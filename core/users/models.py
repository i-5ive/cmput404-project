import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


# https://docs.djangoproject.com/en/2.1/topics/auth/customizing/#using-a-custom-user-model-when-starting-a-project
class Author(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    displayName = models.CharField(max_length=80)
    # TODO URL
    # TODO Friends
    # TODO Host

    # Optional Fields
    github = models.URLField(blank=True, null=True)
    bio = models.TextField(max_length=1024, blank=True, null=True)

    def get_display_name(self):
        return self.displayName
