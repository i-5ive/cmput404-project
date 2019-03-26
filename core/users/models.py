import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

# https://docs.djangoproject.com/en/2.1/topics/auth/customizing/#using-a-custom-user-model-when-starting-a-project

class User(AbstractUser):
    pass
