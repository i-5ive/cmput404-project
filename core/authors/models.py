import uuid

from django.db import models

# Create your models here.
from core.users.models import User


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
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

    def __str__(self):
        return self.user.email
