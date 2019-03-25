from django.db import models
from django.core.validators import RegexValidator

from core.users.models import User


base_url_validator = RegexValidator(r"\/$", "The base URL should not end with a slash.", inverse_match=True)

# Create your models here.
class Server(models.Model):
    # Our Server to Others, Must attach a user (but can block by turning off bools below)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    share_posts = models.BooleanField(default=False)
    share_pictures = models.BooleanField(default=False)

    # Other Servers to Ours (Must add a URL, but maybe not necessary)
    base_url = models.CharField(max_length=250, blank=False, validators=[base_url_validator])
    fetch_posts = models.BooleanField(default=False)
    # Should have a function to check if these are blank, to avoid useless requests
    fetching_username = models.CharField(max_length=250, blank=True)
    fetching_password = models.CharField(max_length=250, blank=True)

    def __str__(self):
        return self.base_url

    def is_server(self):
        return True