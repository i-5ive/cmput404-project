import uuid

from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver

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

class Follow(models.Model):
	follower = models.URLField()
	followed = models.URLField()
	friends = models.BooleanField(default=False)
	
	def __str__(self):
		return self.follower + " is following " + self.followed

class FriendRequest(models.Model):
	requester = models.URLField()
	friend = models.URLField()
	
	def __str__(self):
		return self.requester + " wants to follow " + self.friend

@receiver(post_save, sender=get_user_model())
def create_author_profile(sender, instance, created, **kwargs):
    """
    Create an author profile when a user signs up.
    https://stackoverflow.com/a/12615339 - Michael Bylstra 02/09/2019
    :param sender:
    :param instance:
    :param created:
    :param kwargs:
    :return:
    """
    if created:
        author, new = Author.objects.get_or_create(user=instance)
