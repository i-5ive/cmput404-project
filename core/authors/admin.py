from django.contrib import admin

# Register your models here.
from core.authors.models import Author, Follow

admin.site.register(Author)
admin.site.register(Follow)