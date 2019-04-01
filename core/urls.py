"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import re_path, include
from rest_framework.documentation import include_docs_urls

from core.authors.friend_request_view import handle_follow_request as friend_request
from core.authors.login_view import login
from core.authors.unfollow_author_view import handle_unfollow_request

urlpatterns = [
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^users/', include('core.users.urls')),
    re_path(r'^author/', include('core.authors.urls')),
    re_path(r'^posts/', include('core.posts.urls')),
    re_path(r'^api-auth/', include('rest_framework.urls')),
    re_path(r'^docs/', include_docs_urls(title='API Documentation')),
    re_path(r'^friendrequest\/?', friend_request, name='friendrequest'),
    re_path(r'^login/', login, name='login'),
    re_path(r'^unfollow\/?', handle_unfollow_request, name='unfollow'),
]
