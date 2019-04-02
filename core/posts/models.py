import uuid

from django.db import models
from django.contrib.postgres.fields import ArrayField

# Create your models here.
from core.authors.models import Author


class CommonData(models.Model):

    CONTENT_CHOICES = (
        ('text/markdown', 'Markdown'),
        ('text/plain', 'Plaintext'),
        ('application/base64', 'Application'),
        ('image/png;base64', 'PNG Image'),
        ('image/jpeg;base64', 'JPEG Image')
    )

    contentType = models.CharField(
        max_length=40,
        choices=CONTENT_CHOICES,
        default="text/markdown"
    )

    published = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
        ordering = ['-published']
    
class Posts(CommonData):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # the same post_id is used to identify linked posts for images 
    post_id = models.UUIDField(primary_key=False, default=uuid.uuid4, editable=True)
    title = models.CharField(max_length=100, blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    unlisted = models.BooleanField(default=False)
    visibleTo = ArrayField(models.URLField(), default=list)
    source = models.URLField(blank=True, null=True)
    origin = models.URLField(blank=True, null=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    # DO NOT CHANGE THIS WITHOUT CHANGING EVERYTHING THAT USES THESE...
    VISIBILITY_CHOICES = (
        ('PUBLIC', 'Public'),
        ('FOAF', 'Friend of a Friend'),
        ('FRIENDS', 'Friends'),
        ('PRIVATE', 'Private'),
        ('SERVERONLY', 'Server Only')
    )

    visibility = models.CharField(
        max_length=10,
        choices=VISIBILITY_CHOICES,
        default='PUBLIC'
    )

    # Optional Fields?
    description = models.CharField(max_length=100, blank=True, null=True)
    categories = ArrayField(models.CharField(max_length=200), default=list)

class Comments(CommonData):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    post = models.ForeignKey(Posts, related_name='comments', on_delete=models.CASCADE)
    comment = models.TextField()
    author = models.URLField()
