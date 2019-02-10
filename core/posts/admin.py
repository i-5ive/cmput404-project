from django.contrib import admin

# Register your models here.
from core.posts.models import Posts

admin.site.register(Posts)
