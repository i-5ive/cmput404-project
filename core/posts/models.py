import uuid

# from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver

from core.authors.models import Author

class Posts(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post_id = models.UUIDField(primary_key=False, default=uuid.uuid4, editable=False)
    source_url = models.URLField()
    origin_url = models.URLField()
    content_type = models.CharField(max_length=30)
    title = models.CharField(max_length=100) # can this be blank?
    text_content = models.TextField(blank=True, null=True)
    image_content = models.ImageField(blank=True, null=True)


    # Optional Fields
    description = models.CharField(max_length=100, blank=True, null=True)
