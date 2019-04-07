from django.contrib import admin

# Register your models here.
from core.servers.models import Server

admin.site.register(Server)