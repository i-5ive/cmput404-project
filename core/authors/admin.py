from django.contrib import admin

# Register your models here.
from core.authors.models import Author

admin.site.register(Author)
