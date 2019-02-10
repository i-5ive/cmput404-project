from django.contrib import admin

# Register your models here.
from core.posts.models import Posts
from core.posts.models import Comments

admin.site.register(Posts)
admin.site.register(Comments)
