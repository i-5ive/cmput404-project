from django.contrib import admin

# Register your models here.
from core.authors.models import Author, Follow, FriendRequest

admin.site.register(Author)
admin.site.register(Follow)
admin.site.register(FriendRequest)