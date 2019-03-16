from rest_framework import serializers

from core.authors.models import Author
from core.users.serializers import UserSerializer
from core.hostUtil import get_host_url

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
