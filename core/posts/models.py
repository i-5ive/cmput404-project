import uuid

from django.db import models
from django.contrib.postgres.fields import ArrayField

# Create your models here.
from core.authors.models import Author


class CommonData(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    content_type = models.CharField(max_length=30, default="text/markdown")
    published_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
    
class Posts(CommonData):
    post_id = models.UUIDField(primary_key=False, default=uuid.uuid4, editable=False)
    source_url = models.URLField()
    origin_url = models.URLField()
    title = models.CharField(max_length=100) # can this be blank?
    content = models.TextField(blank=True, null=True)
    unlisted = models.BooleanField(default=False)
    # visible_to is a list of authors
    visible_to = ArrayField(models.CharField(max_length=100), default=list)

    VISIBILITY_CHOICES = (
        ('PUBLIC', 'Public'),
        ('FOAF', 'Friend of a Friend'),
        ('FRIENDS', 'Friends'),
        ('PRIVATE', 'Private'),
        ('SERVERONLY', 'Local Friend')
    )

    visibility = models.CharField(
        max_length=10,
        choices=VISIBILITY_CHOICES,
        default='PUBLIC'
    )

    # Optional Fields
    description = models.CharField(max_length=100, blank=True, null=True)
    categories = ArrayField(models.CharField(max_length=200), default=list)

class Comments(CommonData):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    post = models.ForeignKey(Posts, related_name='comments', on_delete=models.CASCADE)
    comment = models.TextField()
