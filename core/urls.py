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
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from rest_framework.documentation import include_docs_urls

from core.authors.friend_request_view import handle_follow_request as friend_request
from core.authors.login_view import login
from core.authors.unfollow_author_view import handle_unfollow_request
from core.views import get_indexjs

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('core.users.urls')),
    path('author/', include('core.authors.urls')),
    path('posts/', include('core.posts.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('docs/', include_docs_urls(title='API Documentation')),
    path('friendrequest/', friend_request, name='friendrequest'),
    path('login/', login, name='login'),
    path('unfollow/', handle_unfollow_request, name='unfollow'),
    path('index_bundle.js', get_indexjs),
    re_path(r'^', TemplateView.as_view(template_name='index.html')),
]
