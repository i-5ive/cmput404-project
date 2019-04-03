from rest_framework import serializers

from core.authors.models import Author
from core.users.serializers import UserSerializer
from core.hostUtil import get_host_url, is_external_host
from core.servers.SafeServerUtil import ServerUtil
from core.authors.util import get_author_id

class AuthorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Author
        fields = ('id', 'github', 'bio', 'user')

    user = UserSerializer()

class AuthorSummarySerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.URLField()
    host = serializers.URLField()
    id = serializers.URLField()

    class Meta:
        model = Author
        fields = ('id', 'host', 'displayName', 'github', 'url')

def get_summary(instance):
    url = instance.get_url()
    summary = {
        "host": get_host_url(),
        "url": url,
        "id": url,
        "displayName": instance.get_display_name()
    }
    if (instance.github):
        summary["github"] = instance.github
    return summary

def get_external_author_summary(authorUrl):
    # open a server util with the author url
    try:
        sUtil = ServerUtil(authorUrl=authorUrl)
        if not sUtil.valid_server():
            print("authorUrl found, but not in DB", authorUrl)
            raise Exception("Invalid server")
        # split the id from the URL and ask the external server about them
        success, authorInfo = sUtil.get_author_info(authorUrl.split("/author/")[1])
        if not success:
            raise Exception("Could not get author details")
    except Exception as e:
        print(e)
        return {
            "id": "",
            "host": "",
            "url": "",
            "displayName": ""
        }

    return {
        "id": authorUrl,
        "host": sUtil.get_base_url(),
        "url": authorUrl,
        "displayName": authorInfo["displayName"]
    }

def get_author_summary_from_url(url):
    if (is_external_host(url)):
        return get_external_author_summary(url)
    id = get_author_id(url)
    author = Author.objects.get(pk=id)
    return get_summary(author)
