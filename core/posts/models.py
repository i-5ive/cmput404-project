import uuid

from django.db import models
from django.contrib.postgres.fields import ArrayField

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
    published_time = models.DateTimeField(auto_now_add=True, blank=True)
    unlisted = models.BooleanField(default=False)
    visible_to = ArrayField(models.CharField(max_length=100), blank=True, null=True)

    VISIBILITY_CHOICES = (
        ('PUBLIC', 'Public'),
        ('FOAF', 'Friend of a Friend'),
        ('FRIENDS', 'Friends'),
        ('PRIVATE', 'Private'),
        ('SERVERONLY', 'Local Friend')
    )

    visibility = models.CharField(
        max_length=2,
        choices=VISIBILITY_CHOICES,
        default='PUBLIC'
    )

    # TODO Comments!



    # Optional Fields
    description = models.CharField(max_length=100, blank=True, null=True)
    categories = ArrayField(models.CharField(max_length=200), blank=True, null=True)
